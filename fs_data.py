"""get data from 3 files for region, forest and district, and trail data"""

# import Python modules
from csv import DictReader
import geojson
import re

#---------------------------------------------------------------------#

# FOR SEEDING IN SEED.PY
# regions = fs_data.get_regions_list(fs_data.region_file)
# forests, districts = fs_data.get_forests_districts_lists(fs_data.forest_district_file)
# trails, trail_points = fs_data.get_trails_trail_points_lists(fs_data.trail_file)



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
            forests.append({'forest_id': forest_id, 'region_id': region_id, 'forest_name': row['FORESTNAME']})
            districts.append({'district_id': district_id, 'forest_id': forest_id, 'region_id': region_id, 'district_name': row['DISTRICTNAME']  })
    return [forests, districts]

# current location of FS Trails KML File

trail_file = 'seed_data/National_Forest_System_Trails_(Feature_Layer).geojson'
# trails, trail_points = fs_data.get_trails_trail_points_lists(fs_data.trail_file)
def get_trails_trail_points_lists(trail_file):
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
                               'district_id': trail['properties']['ADMIN_ORG']})
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
    

    