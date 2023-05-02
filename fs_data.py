"""get data for region, forest and district, and trail data"""

# import Python modules
from bs4 import BeautifulSoup
from csv import DictReader
import geojson
import re

# import local modules
import crud
import model
import helper

#---------------------------------------------------------------------#
# FOR SEEDING IN INTERACTIVE SEED.PY

# regions = fs_data.get_regions_list(fs_data.region_file)
# forests, districts = fs_data.get_forests_districts_lists(fs_data.forest_district_file)
# trails = fs_data.get_trail_list(fs_data.trail_file)

#---------------------------------------------------------------------#
# SOURCE FILES

region_file = 'seed_data/FS_Regions.csv'
forest_district_file = 'seed_data/FS_Ranger_District_Boundaries.csv'
trail_file = 'seed_data/National_Forest_System_Trails_(Feature_Layer).geojson'
region_geojson = 'seed_data/Forest_Service_Regional_Boundaries_(Feature_Layer).geojson'
forest_geojson = 'seed_data/Forest_Administrative_Boundaries_(Feature_Layer).geojson'
district_geojson = 'seed_data/Ranger_District_Boundaries_(Feature_Layer).geojson'

#---------------------------------------------------------------------#
# OPEN FILES

def get_geojson(file):
    """get geojson"""
    with open(file) as file:
        geojson_info = geojson.load(file)
    return geojson_info

def get_soup_from_file(kml_file):
    """get soup from kml file"""
    with open(kml_file) as file:
        return BeautifulSoup(file, 'xml')
    
#---------------------------------------------------------------------#
# SEED FUNCTIONS

def get_regions_list(file):
    """get list for seeding regions"""
    with open(file) as file:
        region_info = DictReader(file, delimiter='\t')
        regions = []
        for region in region_info:
            long, lat = helper.get_lnglat_for_place(region['Headquarters'])
            regions.append({'region_id': region['Region'], 
                            'region_name': region['Name'],
                            'long': long,
                            'lat': lat
                            })
    return regions


def get_forests_districts_lists(file):
    """get lists for seeding forests and districts"""
    with open(file) as file:
        forest_info = DictReader(file, delimiter=',')
        forests = []
        districts = []
        for row in forest_info:
            region_id = row['REGION']
            forest_num = row['FORESTNUMBER']
            district_num = row['DISTRICTNUMBER']
            forest_id = region_id + forest_num
            district_id = forest_id + district_num
            flong, flat = helper.get_lnglat_for_place(row['FORESTNAME'])
            forests.append({'forest_id': forest_id, 
                            'region_id': region_id, 
                            'forest_name': row['FORESTNAME'], 
                            'is_forest_empty': False,
                            'long': flong,
                            'lat': flat
                            })
            dlnglat = helper.get_lnglat_for_place(row['DISTRICTNAME'])
            if dlnglat:
                dlong, dlat = dlnglat
            else:
                dlong = flong
                dlat = flat
            districts.append({'district_id': district_id, 
                            'forest_id': forest_id, 
                            'region_id': region_id, 
                            'district_name': row['DISTRICTNAME'],
                            'is_district_empty': False,
                            'long': dlong,
                            'lat': dlat})
    return [forests, districts]

def get_trail_list(trail_file):
    """get list for seeding trails"""
     
    trailset = get_geojson(trail_file)
    trails = []
    district_ids = set(crud.get_district_ids())
    for trail in trailset[:]:
        if (trail['properties']['ADMIN_ORG'] and 
            trail['properties']['TRAIL_NAME'] and
            trail['properties']['TRAIL_CN'] not in [trail['trail_id'] for trail in trails] and
            len(trail['properties']['ADMIN_ORG']) == 6 and
            trail['properties']['ADMIN_ORG'] in district_ids
            ):
            if (trail['geometry']['coordinates'] and 
                type(trail['geometry']['coordinates'][0][0]) == float
                ):
                th_long = trail['geometry']['coordinates'][0][0]
                th_lat = trail['geometry']['coordinates'][0][1]
            else:
                district = crud.get_district_by_id(trail['properties']['ADMIN_ORG'])
                th_long = district.long
                th_lat = district.lat
            trails.append({'trail_id': trail['properties']['TRAIL_CN'], 
                           'trail_no': trail['properties']['TRAIL_NO'], 
                           'trail_name': trail['properties']['TRAIL_NAME'], 
                           'region_id': trail['properties']['ADMIN_ORG'][:2], 
                           'forest_id': trail['properties']['ADMIN_ORG'][:4], 
                           'district_id': trail['properties']['ADMIN_ORG'],
                           'is_trail_empty': False,
                           'th_long': th_long,
                           'th_lat': th_lat
                           })

    return trails
    

# def get_region_places(region_coord_file=region_coord_file):
#     """get list of coordinate dictionaries for each region"""
    
#     soup = get_soup_from_file(region_coord_file)

#     placemarks = soup.find_all('Placemark') 
#     region_places = []       
#     for placemark in placemarks[:]:
#         id = placemark.select_one('[name="REGION"]').text
#         hq = placemark.select_one('[name="REGIONHEADQUARTERS"]').text
#         region_places.append({'id': id, 'place': hq})
#     return region_places

#---------------------------------------------------------------------#
# GEOJSON FUNCTIONS


# region_json = fs_data.get_geojson(fs_data.region_file)
# forest_json = fs_data.get_geojson(fs_data.forest_file)
# district_json = fs_data.get_geojson(fs_data.district_file)
# trail_json = fs_data.get_geojson(fs_data.trail_file)

def get_forests_geojson_for_region(file=forest_geojson, region_id='03'):
    geojson = get_geojson(file)
    newfeatures = []
    for feature in geojson['features']:
        if feature['properties']['REGION'] == region_id:
            newfeatures.append(feature)
    geojson['features'] = newfeatures
    return geojson

def get_districts_geojson_for_forest(file=district_geojson, forest_id='0301'):
    geojson = get_geojson(file)
    newfeatures = []
    for feature in geojson['features']:
        forest_num = feature['properties']['REGION'] + feature['properties']['FORESTNUMBER']
        if  forest_num == forest_id:
            newfeatures.append(feature)
    geojson['features'] = newfeatures
    return geojson


def get_trails_geojson_for_district(file=trail_file, district_id='030102'):
    geojson = get_geojson(file)
    newfeatures = []
    for feature in geojson['features']:
        if feature['properties']['ADMIN_ORG'] == district_id:
            newfeatures.append(feature)
    geojson['features'] = newfeatures
    return geojson

def get_trail(file=trail_file, trail_id="11631010437"):
    geojson = get_geojson(file)
    newfeatures = []
    for feature in geojson['features']:
        if feature['properties']['TRAIL_CN'] == trail_id:
            newfeatures.append(feature)
    geojson['features'] = newfeatures
    return geojson