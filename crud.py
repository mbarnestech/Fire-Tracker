# import Python modules
from datetime import datetime

# import local modules
from model import Trail, TrailPoint, Fire, connect_to_db, db


# CRUD functions

# def create_trail(name, trail_url, gpx_url, miles, high_elevation, low_elevation, elevation_gain, trail_type, difficulty, last_condition, last_condition_update, last_condition_notes, stars, votes, state, area, subarea, city, dogs):
def create_trail(trail_name, hp_id, state, area, city):
    """Create and return a new trail."""
    return Trail(trail_name=trail_name, hp_id=hp_id, state=state, area=area, city=city)


def create_trail_point(trail, latitude, longitude):
    """Create and return a new trail point"""
    return TrailPoint(trail=trail, latitude=latitude, longitude=longitude)


def create_fire(fire_url, fire_name, latitude, longitude, incident_type, last_updated, size, contained):
    """Create and return a new fire."""
    return Fire(fire_url=fire_url, fire_name=fire_name, latitude=latitude, longitude=longitude, incident_type=incident_type, last_updated=last_updated, size=size, contained=contained)


# Connect to database when running crud.py interactively
if __name__ == '__main__':
    from server import app
    connect_to_db(app)
