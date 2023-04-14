"""CRUD functions live here"""

# import local modules
from model import Region, Forest, District, Trail, TrailPoint, Fire, connect_to_db
import helper

#---------------------------------------------------------------------#
# CREATE

def create_region(region_id, region_name):
    """Create and return a new region."""
    return Region(region_id=region_id, region_name=region_name)

def create_forest(forest_id, forest_name, region):
    """Create and return a new forest."""
    return Forest(forest_id=forest_id, forest_name=forest_name, region=region)

def create_district(district_id, district_name, region, forest):
    """Create and return a new district."""
    return District(district_id=district_id, district_name=district_name, region=region, forest=forest)

def create_trail(trail_id, trail_no, trail_name, region, forest, district):
    """Create and return a new trail."""
    return Trail(trail_id=trail_id, trail_no=trail_no, trail_name=trail_name, region=region, forest=forest, district=district)


def create_trail_point(trail, latitude, longitude):
    """Create and return a new trail point"""
    return TrailPoint(trail=trail, latitude=latitude, longitude=longitude)


def create_fire(fire_url, fire_name, latitude, longitude, incident_type, last_updated, size, contained):
    """Create and return a new fire."""

    decimal_latitude = helper.create_decimal_latlong(latitude)
    decimal_longitude = helper.create_decimal_latlong(longitude)

    return Fire(fire_url=fire_url, fire_name=fire_name, latitude=decimal_latitude, longitude=decimal_longitude, incident_type=incident_type, last_updated=last_updated, size=size, contained=contained)

#---------------------------------------------------------------------#

# Connect to database when running crud.py interactively
if __name__ == '__main__':
    from server import app
    connect_to_db(app)
