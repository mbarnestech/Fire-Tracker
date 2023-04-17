# import Python modules
import os
from datetime import datetime

# import local modules
import crud
import model
import server
import fs_data
import fire_data

#---------------------------------------------------------------------#
def regenerate_db():
    """run to delete fire_tracker db from system and replace with structure from model.py"""

    # delete fire_tracker db if it exists
    os.system('dropdb --if-exists fire_tracker')
    # create new fire_tracker db
    os.system('createdb fire_tracker')
    # with server.app.app_context():
    model.connect_to_db(server.app)
    # add structure to database
    model.db.create_all()

#---------------------------------------------------------------------#

def seed_regions(regions):
    """for a given region, create Region instance and add it to the db session"""
    
    for region in regions:
        if model.Region.query.filter_by(region_id = region['region_id']).first():
            continue
        model.db.session.add(crud.create_region(region['region_id'], 
                                                region['region_name']
                                                ))
        
    model.db.session.commit()


def seed_forests(forests):
    """for a given forest, create Forest instance and add it to the db session"""
    for forest in forests:
        if model.Forest.query.filter_by(forest_id = forest['forest_id']).first():
            continue
        model.db.session.add(crud.create_forest(forest['forest_id'], 
                                                forest['forest_name'],
                                                forest['region_id']
                                                ))
    model.db.session.commit()


def seed_districts(districts):
    """for a given district, create District instance and add it to the db session"""
    for district in districts:
        if model.District.query.filter_by(district_id = district['district_id']).first():
            continue
        model.db.session.add(crud.create_district(district['district_id'], 
                                                  district['district_name'],
                                                  district['region_id'],
                                                  district['forest_id']
                                                  ))
        
    model.db.session.commit()


def seed_trails(trails):
    """for a given trail, create Trail instance and add it to the db session"""
    
    for trail in trails:
        if (model.Trail.query.filter_by(trail_id = trail['trail_id']).first()
            or not model.District.query.filter_by(district_id = trail['district_id']).first()):
            continue
        model.db.session.add(crud.create_trail(
                                            trail['trail_id'],
                                            trail['trail_no'],
                                            trail['trail_name'], 
                                            trail['region_id'],
                                            trail['forest_id'], 
                                            trail['district_id']
                                            ))
    # commit to db
    model.db.session.commit()


# # Create function for seeding trail point data
def seed_trail_points(trail_points):
    """for a given trail point, create TrailPoint instance and add it to the db session"""
    for trail_point in trail_points:
        if model.Trail.query.filter_by(trail_id = trail_point['trail_id']).first():
            model.db.session.add(crud.create_trail_point(trail_point['trail_id'], 
                                        trail_point['latitude'],
                                        trail_point['longitude']
                                        ))
    model.db.session.commit()


# Sample fire data (3 most recent fires from inciweb_placemarks.kml)
# fires = [{'fire_url': 'https://inciweb.wildfire.gov/incident-information/copsf-403-fire', 
#         'fire_name': '403 Fire', 
#         'latitude': '38 .5212', 
#         'longitude': '-105.2248', 
#         'incident_type': 'Wildfire', 
#         'last_update': datetime(2023, 4, 3), 
#         'size': 1518, 
#         'contained': 60}, 
#         {'fire_url': 'https://inciweb.wildfire.gov/incident-information/aza3s-texas-summit-fire', 
#         'fire_name': 'Texas Summit Fire', 
#         'latitude': '32 .0313.4', 
#         'longitude': '-110 .0454.1', 
#         'incident_type': 'Wildfire', 
#         'last_update': datetime(2023, 3, 31), 
#         'size': 455, 
#         'contained': 80},
#         {'fire_url': 'https://inciweb.wildfire.gov/incident-information/wvmof-hopkins-knob-prescribed-burn', 
#         'fire_name': 'Hopkins Knob Prescribed Burn', 
#         'latitude': '37.5717', 
#         'longitude': '-80.1455.6', 
#         'incident_type': 'Prescribed Fire', 
#         'last_update': datetime(2023, 3, 30), 
#         'size': 837, 
#         'contained': None 
#         }]

# # Create function for seeding fire data
def seed_fires(fires):
    """for a given fire, create Fire instance and add it to the db session"""
    for fire in fires:
        model.db.session.add(crud.create_fire(fire['fire_url'],
                                    fire['fire_name'],
                                    fire['latitude'],
                                    fire['longitude'],
                                    fire['incident_type'],
                                    fire['last_updated'],
                                    fire['size'],
                                    fire['contained']
                                    ))
    model.db.session.commit()