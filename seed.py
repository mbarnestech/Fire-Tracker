# import Python modules
import os
from datetime import datetime

# import local modules
import crud
import model
import server
import trails

#---------------------------------------------------------------------#
# delete fire_tracker db if it exists
os.system('dropdb --if-exists fire_tracker')
# create new fire_tracker db
os.system('createdb fire_tracker')

# connect to db
# with server.app.app_context():
model.connect_to_db(server.app)
# add structure to database
model.db.create_all()

#---------------------------------------------------------------------#

# Sample trail data (2 trails; real data from HikingProject.com, manually cleaned to conform to data types wanted)
trails_list = [{'trail_name': 'Cochise Stronghold Trail #279', 
        'hp_id': '7030929', 
        'state': 'AZ',
        'area': 'Southern Arizona and Tucson',
        'city': 'Saint David'},
        {'trail_name': 'Roundup Ground Trail (T107)', 
        'hp_id': '7025732',    
        'state': 'NM',
        'area': 'Southwestern New Mexico',
        'city': 'Alamogordo'
        }]


# Create function for seeding trail data, commented out as db has this info
def seed_trails(trails):
    """for a given trail, create Trail instance and add it to the db session"""
    
    for trail in trails:
        if model.Trail.query.filter_by(hp_id = trail['hp_id']).first():
            continue
        model.db.session.add(crud.create_trail(trail['trail_name'], 
                                            trail['hp_id'],
                                            trail['state'], 
                                            trail['area'],
                                            trail['city'] 
                                            ))
    # commit to db
    model.db.session.commit()


# Populate session data with trails

seed_trails(trails.trails)
seed_trails(trails_list)


# Create sample trail point data (3 trail points from each trail taken from gpx files)
cochise = model.Trail.query.filter_by(hp_id = '7030929').one()
roundup = model.Trail.query.filter_by(hp_id = '7025732').one()

trail_points = [{'trail': cochise,
                'latitude': 31.92212,
                'longitude': -109.967257},
                {'trail': cochise,
                'latitude': 31.921998,
                'longitude': -109.96714},
                {'trail': cochise,
                'latitude': 31.907548,
                'longitude': -109.967176},
                {'trail': roundup,
                'latitude': 32.859774,
                'longitude': -105.910034},
                {'trail': roundup,
                'latitude': 32.859147,
                'longitude': -105.906862},
                {'trail': roundup,
                'latitude': 32.854016,
                'longitude': -105.90229}]  

# # Create function for seeding trail point data
def seed_trail_points(trail_points):
    """for a given trail, create Trail instance and add it to the db session"""
    for trail_point in trail_points:
        model.db.session.add(crud.create_trail_point(trail_point['trail'], 
                                    trail_point['latitude'],
                                    trail_point['longitude']
                                    ))
    model.db.session.commit()

# Populate session data with trail points
seed_trail_points(trail_points)


# Sample fire data (3 most recent fires from inciweb_placemarks.kml)

fires = [{'fire_url': 'https://inciweb.wildfire.gov/incident-information/copsf-403-fire', 
        'fire_name': '403 Fire', 
        'latitude': '38 .5212', 
        'longitude': '-105.2248', 
        'incident_type': 'Wildfire', 
        'last_update': datetime(2023, 4, 3), 
        'size': 1518, 
        'contained': 60}, 
        {'fire_url': 'https://inciweb.wildfire.gov/incident-information/aza3s-texas-summit-fire', 
        'fire_name': 'Texas Summit Fire', 
        'latitude': '32 .0313.4', 
        'longitude': '-110 .0454.1', 
        'incident_type': 'Wildfire', 
        'last_update': datetime(2023, 3, 31), 
        'size': 455, 
        'contained': 80},
        {'fire_url': 'https://inciweb.wildfire.gov/incident-information/wvmof-hopkins-knob-prescribed-burn', 
        'fire_name': 'Hopkins Knob Prescribed Burn', 
        'latitude': '37.5717', 
        'longitude': '-80.1455.6', 
        'incident_type': 'Prescribed Fire', 
        'last_update': datetime(2023, 3, 30), 
        'size': 837, 
        'contained': None 
        }]

# # Create function for seeding fire data
def seed_fires(fires):
    """for a given trail, create Trail instance and add it to the db session"""
    for fire in fires:
        model.db.session.add(crud.create_fire(fire['fire_url'],
                                    fire['fire_name'],
                                    fire['latitude'],
                                    fire['longitude'],
                                    fire['incident_type'],
                                    fire['last_update'],
                                    fire['size'],
                                    fire['contained']
                                    ))
        model.db.session.commit()

# Populate session data with fires
seed_fires(fires)