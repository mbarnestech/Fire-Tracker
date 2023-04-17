"""CRUD functions live here"""

# import local modules
from model import Region, Forest, District, Trail, TrailPoint, Fire, db, connect_to_db
import helper
import fire_data


#---------------------------------------------------------------------#
# CREATE

def create_region(region_id, region_name):
    """Create and return a new region."""
    return Region(region_id=region_id, region_name=region_name)


def create_forest(forest_id, forest_name, region_id):
    """Create and return a new forest."""
    return Forest(forest_id=forest_id, forest_name=forest_name, region_id=region_id)


def create_district(district_id, district_name, region_id, forest_id):
    """Create and return a new district."""
    return District(district_id=district_id, district_name=district_name, region_id=region_id, forest_id=forest_id)


def create_trail(trail_id, trail_no, trail_name, region_id, forest_id, district_id):
    """Create and return a new trail."""
    return Trail(trail_id=trail_id, trail_no=trail_no, trail_name=trail_name, region_id=region_id, forest_id=forest_id, district_id=district_id)


def create_trail_point(trail_id, latitude, longitude):
    """Create and return a new trail point"""
    return TrailPoint(trail_id=trail_id, latitude=latitude, longitude=longitude)


def create_fire(fire_url, fire_name, latitude, longitude, incident_type, last_updated, size, contained, db_updated):
    """Create and return a new fire."""

    return Fire(fire_url=fire_url, fire_name=fire_name, latitude=latitude, longitude=longitude, incident_type=incident_type, last_updated=last_updated, size=size, contained=contained, db_updated=db_updated)


#---------------------------------------------------------------------#
# READ

def get_regions():
    """return a list of all Region objects"""
    return Region.query.all()


def get_forests():
    """return a list of all Forest objects"""
    return Forest.query.all()


def get_fires():
    """return a list of all Fire objects"""
    return Fire.query.all()

def get_region_names():
    """return a list of all region names"""
    return [region[0] for region in db.session.query(Region.region_name).all()]


def get_forests_by_region_name(chosen_region_name):
    return [forest[0] for forest in db.session.query(Forest.forest_name).join(Region).filter(Region.region_name == chosen_region_name).all()]

def get_districts_by_forest_name(chosen_forest_name):
    return [district[0] for district in db.session.query(District.district_name).join(Forest).filter(Forest.forest_name == chosen_forest_name).all()]

def get_trails_by_district_name(chosen_district_name):
    return [trail[0] for trail in db.session.query(Trail.trail_name).join(District).filter(District.district_name == chosen_district_name).all()]

def get_trail_with_trail_name(trail_name):
    """return single Trail instance with trail_name attribute"""
    return Trail.query.filter_by(trail_name = trail_name).one()


def get_trailpoint_list_with_trail_id(trail_id):
    """return a list of TrailPoint objects corresponding to a trail id"""
    return db.session.query(TrailPoint).filter(TrailPoint.trail_id == trail_id).all()


def get_fires_with_fire_ids(fires):
    """get list of Fire objects corresponding to list of fire_id numbers"""
    fire_list = []
    for fire in fires:
        fire_list.append(Fire.query.filter(Fire.fire_id == fire.fire_id).one())
    return fire_list

def get_last_db_update():
    return db.session.query(Fire.db_updated).order_by(Fire.db_updated.desc()).first()[0]


#---------------------------------------------------------------------#
# UPDATE

def update_fires():
    from datetime import date

    fires = fire_data.get_fires()
    
    for fire in fires:
        if Fire.query.filter_by(fire_url = fire['fire_url']).first():
            fire_to_update = Fire.query.filter_by(fire_url = fire['fire_url']).first()
            fire_to_update.last_updated = fire['last_updated']
            fire_to_update.db_updated = fire['db_updated']
        else:
            db.session.add(create_fire(
                fire['fire_url'],
                fire['fire_name'],
                fire['latitude'],
                fire['longitude'],
                fire['incident_type'],
                fire['last_updated'],
                fire['size'],
                fire['contained'],
                fire['db_updated']
                ))
    db.session.commit()
    

#---------------------------------------------------------------------#

# Connect to database when running crud.py interactively
if __name__ == '__main__':
    from server import app
    connect_to_db(app)
