"""get data for region, forest and district, and trail data"""

# import Python modules
from csv import DictReader
import geojson
import re
from bs4 import BeautifulSoup

import crud

#---------------------------------------------------------------------#

# FOR SEEDING IN SEED.PY
# regions = fs_data.get_regions_list(fs_data.region_file)
# forests, districts = fs_data.get_forests_districts_lists(fs_data.forest_district_file)
# trails, trail_points = fs_data.get_trails_trail_points_lists(fs_data.trail_file)
# coords = fs_data.get_region_coords()



# current location of region csv file
region_file = 'seed_data/FS_Regions.csv'

def get_regions_list(region_file):
    with open(region_file) as file:
        csv_reader = DictReader(file, delimiter='\t')
        regions = []
        for region in csv_reader:
            regions.append({'region_id': region['Region'], 'region_name': region['Name']})
    return regions

# current location of district csv file
forest_district_file = 'seed_data/FS_Ranger_District_Boundaries.csv'

def get_forests_districts_lists(forest_district_file):
    with open(forest_district_file) as file:
        csv_reader = DictReader(file)
        forests = []
        districts = []
        for row in csv_reader:
            region_id = row['REGION']
            forest_num = row['FORESTNUMBER']
            district_num = row['DISTRICTNUMBER']
            forest_id = region_id + forest_num
            district_id = forest_id + district_num            
            forests.append({'forest_id': forest_id, 'region_id': region_id, 'forest_name': row['FORESTNAME'], 'is_forest_empty': False})
            districts.append({'district_id': district_id, 'forest_id': forest_id, 'region_id': region_id, 'district_name': row['DISTRICTNAME'],'is_district_empty': False})
    return [forests, districts]

# current location of FS Trails geojson File
trail_file = 'seed_data/National_Forest_System_Trails_(Feature_Layer).geojson'

def get_trails_trail_points_lists(trail_file):
    """get list for seeding both trails and trail points"""
    with open(trail_file) as file:
        trailset = geojson.load(file)
        trails = []
        trail_points = []
        for trail in trailset[:]:
            if (trail['properties']['ADMIN_ORG'] and 
                trail['properties']['TRAIL_NAME'] and
                trail['properties']['TRAIL_CN'] not in [trail['trail_id'] for trail in trails] and
                len(trail['properties']['ADMIN_ORG']) == 6
                ):
                trails.append({'trail_id': trail['properties']['TRAIL_CN'], 
                               'trail_no': trail['properties']['TRAIL_NO'], 
                               'trail_name': trail['properties']['TRAIL_NAME'], 
                               'region_id': trail['properties']['ADMIN_ORG'][:2], 
                               'forest_id': trail['properties']['ADMIN_ORG'][:4], 
                               'district_id': trail['properties']['ADMIN_ORG'],
                               'is_trail_empty': False})
                for coordinate in trail['geometry']['coordinates']:
                    if type(coordinate[0]) == float and type(coordinate[1]) == float:
                        trail_points.append({'trail_id': trail['properties']['TRAIL_CN'],
                                            'longitude': coordinate[0],
                                            'latitude': coordinate[1]})
                    else:
                        removed = trails.pop()
                        print(f'***** REMOVED ****** {removed}')
                        break

    return [trails, trail_points]

def get_trails_only(trail_file):
    """get list for seeding only trails"""
    with open(trail_file) as file:
        trailset = geojson.load(file)
        trails = []
        for trail in trailset[:]:
            if (trail['properties']['ADMIN_ORG'] and 
                trail['properties']['TRAIL_NAME'] and
                trail['properties']['TRAIL_CN'] not in [trail['trail_id'] for trail in trails] and
                len(trail['properties']['ADMIN_ORG']) == 6
                ):
                trails.append({'trail_id': trail['properties']['TRAIL_CN'], 
                               'trail_no': trail['properties']['TRAIL_NO'], 
                               'trail_name': trail['properties']['TRAIL_NAME'], 
                               'region_id': trail['properties']['ADMIN_ORG'][:2], 
                               'forest_id': trail['properties']['ADMIN_ORG'][:4], 
                               'district_id': trail['properties']['ADMIN_ORG'],
                               'is_trail_empty': False})
                for coordinate in trail['geometry']['coordinates']:
                    if not (type(coordinate[0]) == float and type(coordinate[1]) == float):
                        removed = trails.pop()
                        print(f'***** REMOVED ****** {removed}{coordinate[0]=}{coordinate[1]=}')
                        break

    return trails
    
def get_soup_from_file(kml_file):
    """get soup from kml file"""
    with open(kml_file) as file:
        return BeautifulSoup(file, 'xml')

# current location of regional boundaries kml file
region_coord_file = 'seed_data/Forest_Service_Regional_Boundaries_(Feature_Layer).kml'

def get_region_coords(region_coord_file=region_coord_file):
    """get list of coordinate dictionaries for each region"""
    
    soup = get_soup_from_file(region_coord_file)

    placemarks = soup.find_all('Placemark') 
    region_coords = []       
    for placemark in placemarks[:]:
        coords = placemark.find('coordinates').string[:].split()
        for coord in coords[:]:
            latitude, longitude = coord.split(',')
            region_coords.append({'region_id': placemark.select_one('[name="REGION"]').text,
                                  'latitude': float(latitude),
                                  'longitude': float(longitude)})
    return region_coords


# current location of forest boundaries kml file
forest_coord_file = 'seed_data/Forest_Administrative_Boundaries_(Feature_Layer).kml'

def get_forest_coords(forest_coord_file=forest_coord_file):
    soup = get_soup_from_file(forest_coord_file)
    coords = []
    forest_ids = crud.get_forest_ids()
    placemarks = soup.find_all('Placemark') 
    for placemark in placemarks[:1]:
        if placemark.select_one('[name="FORESTORGCODE"]').text in forest_ids:
            polygons = placemark.find_all('coordinates')
            count = 1
            if polygons:
                for polygon in polygons[:]:
                    coords = polygon.string[:].split()
                    for coord in coords[:]:
                        latitude, longitude = coord.split(',')
                        coords.append({'forest_id': placemark.select_one('[name="FORESTORGCODE"]').text,
                                       'polygon_no': count,
                                       'latitude': float(latitude),
                                       'longitude': float(longitude)})
                    count += 1
    return coords
