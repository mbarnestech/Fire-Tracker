"""get data from 3 files for region, forest and district, and trail data"""

# import Python modules
from csv import DictReader

#---------------------------------------------------------------------#

# current location of region csv file
region_file = 'seed_data/FS_Regions.csv'

def get_regions_list(region_file):
    with open(region_file) as file:
        csv_reader = DictReader(file, delimiter='\t')
        regions = []
        for region in csv_reader:
            regions.append({'region_id': region['Region'], 'region_name': region['Name']})
    return regions

# current location of region csv file
forest_district_file = 'seed_data/FS_Ranger_District_Boundaries.csv'
# forests = fs_data.get_forest_district_list(fs_data.forest_district_file)
def get_forest_district_list(forest_district_file):
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
