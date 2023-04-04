# import Python modules
import os
from datetime import datetime

# import local modules
from crud import create_trail, create_trail_point, create_fire
import model
import server

# delete fire_tracker db if it exists
os.system('dropdb --if-exists fire_tracker')
# create new fire_tracker db
os.system('createdb fire_tracker')

# connect to db
model.connect_to_db(server.app)
# add structure to database
model.db.create_all()

# Sample trail data (2 trails; real data from HikingProject.com, manually cleaned to conform to data types wanted)
trails = [{'name': 'Cochise Stronghold Trail #279', 
        'hp_id': '7030929', 
        'state': 'AZ',
        'area': 'Southern Arizona and Tucson',
        'city': 'Saint David'},
        {'name': 'Roundup Ground Trail (T107)', 
        'hp_id': '7025732',    
        'state': 'NM',
        'area': 'Southwestern New Mexico',
        'city': 'Alamogordo'
        }]


# Create function for seeding trail data
def seed_trail(trail):
   """for a given trail, create Trail instance and add it to the db session"""
   model.db.session.add(create_trail(trail['name'], 
                               trail['hp_id'],
                               trail['state'], 
                               trail['area'],
                               trail['city'] 
                               ))

# Populate session data with trails
for trail in trails:
   seed_trail(trail)

# Create sample trail point data (3 trail points from each trail taken from gpx files)
cochise = model.db.session.query(model.Trail).filter(model.Trail.hp_id == '7030929').one()
roundup = db.session.query(model.Trail).filter(model.Trail.hp_id == '7025732').one()

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

# Create function for seeding trail point data
def seed_trail_point(trail_point):
   """for a given trail, create Trail instance and add it to the db session"""
   model.db.session.add(create_trail_point(trail_point['trail'], 
                               trail_point['latitude'],
                               trail_point['longitude']
                               ))

# Populate session data with trail points
for trail_point in trail_points:
   seed_trail(trail_point)

# Sample fire data (3 most recent fires from inciweb_placemarks.kml)

fires = [{'fire_url': 'https://inciweb.wildfire.gov/incident-information/copsf-403-fire', 
        'fire_name': '403 Fire', 
        'latitude': '38 .5212', 
        'longitude': '-105.2248', 
        'incident_type': 'Wildfire', 
        'last_update': datetime.date(2023, 4, 3), 
        'size': 1518, 
        'contained': 60}, 
        {'fire_url': 'https://inciweb.wildfire.gov/incident-information/aza3s-texas-summit-fire', 
        'fire_name': 'Texas Summit Fire', 
        'latitude': '32 .0313.4', 
        'longitude': '-110 .0454.1', 
        'incident_type': 'Wildfire', 
        'last_update': datetime.date(2023, 3, 31), 
        'size': 455, 
        'contained': 80},
        {'fire_url': 'https://inciweb.wildfire.gov/incident-information/wvmof-hopkins-knob-prescribed-burn', 
        'fire_name': 'Hopkins Knob Prescribed Burn', 
        'latitude': '37.5717', 
        'longitude': '-80.1455.6', 
        'incident_type': 'Prescribed Fire', 
        'last_update': datetime.date(2023, 3, 30), 
        'size': 837, 
        'contained': None 
        }]

# Create function for seeding fire data
def seed_fire(fire):
   """for a given trail, create Trail instance and add it to the db session"""
   model.db.session.add(create_fire(fire['fire_url'],
                              fire['fire_name'],
                              fire['latitude'],
                              fire['longitude'],
                              fire['incident_type'],
                              fire['last_update'],
                              fire['size'],
                              fire['contained']
                              ))

# Populate session data with fires
for fire in fires:
   seed_trail(fire)


# save all db session data to database
model.db.session.commit()













# Sample trail data (2 trails; real data from HikingProject.com, manually cleaned to conform to data types wanted)
trail1 = {'name': 'Cochise Stronghold Trail #279', 
        'trail_url': 'https://www.hikingproject.com/trail/7030929/cochise-stronghold-trail-279',  # check a few more trails - looks like there's an id# for the trails that makes the trail and gpx url; could just store that in the database
        'gpx_url': 'https://www.hikingproject.com/trail/gpx/7030929',
        'miles': 4.6,
        'high_elevation': 5962,
        'low_elevation': 4938,
        'elevation_gain': 1026,
        'trail_type': 'Point to Point',
        'difficulty': 'Intermediate/Difficult',
        'last_condition': 'All Clear',
        'last_condition_update': datetime.date(2023, 3, 23),
        'last_condition_notes': None,
        'stars': 4.6,
        'votes': 8,
        'state': 'AZ',
        'area': 'Southern Arizona and Tucson',
        'subarea': 'Coronado National Forest',
        'city': 'Saint David',
        'dogs': 'Leashed'}
trail2 = {'name': 'Roundup Ground Trail (T107)', 
        'trail_url': 'https://www.hikingproject.com/trail/7025732/roundup-ground-trail-t107',    
        'gpx_url': 'https://www.hikingproject.com/trail/gpx/7025732',
        'miles': 2.9,
        'high_elevation': 6002,
        'low_elevation': 4890,
        'elevation_gain': 1112,
        'trail_type': 'Point to Point',
        'difficulty': 'Difficult',
        'last_condition': 'All Clear',
        'last_condition_update': datetime.date(2020, 1, 22),
        'last_condition_notes': 'Dry - Great shape! — ',
        'stars': 3.7,
        'votes': 3,
        'state': 'NM',
        'area': 'Southwestern New Mexico',
        'subarea': 'Alamogordo',
        'city': 'Alamogordo',
        'dogs': 'Off-leash'
        }

# TODO: loop through sample trail data to populate session data
def seed_trail(trail):
   db.session.add(create_trail(trail[name], 
                               trail[trail_url], 
                               trail[gpx_url], 
                               trail[miles], 
                               trail[high_elevation], 
                               trail[low_elevation], 
                               trail[elevation_gain], 
                               trail[trail_type], 
                               trail[difficulty], 
                               trail[last_condition], 
                               trail[last_condition_update], 
                               trail[last_condition_notes], 
                               trail[stars], 
                               trail[votes], 
                               trail[state], 
                               trail[area], 
                               trail[subarea], 
                               trail[city], 
                               trail[dogs]))