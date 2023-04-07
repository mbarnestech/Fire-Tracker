# import Python modules
from datetime import datetime

# import local modules
from model import Trail, TrailPoint, Fire, connect_to_db, db
import helper

#---------------------------------------------------------------------#
# functions to create class instances


def create_trail(trail_name, hp_id, state, area, city):
    """Create and return a new trail."""
    return Trail(trail_name=trail_name, hp_id=hp_id, state=state, area=area, city=city)


def create_trail_point(trail, latitude, longitude):
    """Create and return a new trail point"""
    return TrailPoint(trail=trail, latitude=latitude, longitude=longitude)


def create_fire(fire_url, fire_name, latitude, longitude, incident_type, last_updated, size, contained):
    """Create and return a new fire."""

    decimal_latitude = helper.create_decimal_latlong(latitude)
    decimal_longitude = helper.create_decimal_latlong(longitude)

    return Fire(fire_url=fire_url, fire_name=fire_name, latitude=decimal_latitude, longitude=decimal_longitude, incident_type=incident_type, last_updated=last_updated, size=size, contained=contained)

#---------------------------------------------------------------------#

def get_trail_with_trail_name(trail_name):
    """return single Trail instance with trail_name attribute"""
    return Trail.query.filter_by(trail_name = trail_name).one()


def get_trailpoint_list_with_trail_id(trail_id):
    """return a list of TrailPoint objects corresponding to a trail id"""
    return db.session.query(TrailPoint).filter(Trail.trail_id == trail_id).all()

def get_fires():
    """return a list of all Fire objects"""
    return Fire.query.all()

def get_trails():
    """return a list of all Trail objects"""
    return Trail.query.all()

def get_fires_with_fire_ids(fires):
    """get list of Fire objects corresponding to list of fire_id numbers"""
    fire_list = []
    for fire in fires:
        fire_list.append(Fire.query.filter(Fire.fire_id == fire.fire_id).one())
    return fire_list
    
# Connect to database when running crud.py interactively
if __name__ == '__main__':
    from server import app
    connect_to_db(app)
