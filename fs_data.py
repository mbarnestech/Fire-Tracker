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
