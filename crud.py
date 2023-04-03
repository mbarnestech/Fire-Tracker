# import Python modules
from datetime import datetime

# import local modules
from model import db, Trail, TrailPoint, Fire, connect_to_db


# CRUD functions
def create_trail(name, trail_url, gpx_url, miles, kilometers, high_elevation, low_elevation, total_elevation_gain, trail_type, difficulty, last_condition, last_condition_update, last_condition_notes, stars, state, area, subarea, city,):
    """Create and return a new trail."""
    pass


def create_trail_point(trail, latitude, longitude, elevation):
    """Create and return a new trail point"""
    pass


def create_fire(fire_url, fire_name, latitude, longitude, incident_type, last_updated, size, contained):
    """Create and return a new fire."""
    pass


# Connect to database when running crud.py interactively
if __name__ == '__main__':
    from server import app
    connect_to_db(app)
