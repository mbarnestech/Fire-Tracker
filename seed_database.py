# import Python modules
import os
from datetime import datetime

# import local modules
from crud import create_trail, create_trail_point, create_fire
from model import connect_to_db, db
import server

# delete fire_tracker db if it exists
os.system('dropdb fire_tracker')
# create new fire_tracker db
os.system('createdb fire_tracker')

# connect to db
connect_to_db(server.app)
# add structure to database
db.create_all()

# TODO: create sample trail data (2 trails; real data copied but not yet scraped from hiking project html files)
# TODO: create sample trail point data (3 trail points from each trail taken from gpx files)
# TODO: create sample fire data (3 most recent fires)
# TODO: loop through sample trail data to populate session data
# TODO: loop through sample trail point data to populate session data
# TODO: loop through sample fire data to populate session data
# TODO: remember to add all data to session prior to committing

# save all db session data to database
db.session.commit()