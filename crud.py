"""CRUD functions live here"""

# import local modules
import fire_data
import fs_data
import helper
from model import Region, Forest, District, Trail, Fire, db, connect_to_db


#---------------------------------------------------------------------#
# CREATE

def create_region(region_id, region_name, long, lat):
    """Create and return a new region."""
    return Region(region_id=region_id, region_name=region_name, long=long, lat=lat)

def create_forest(forest_id, forest_name, region_id, is_forest_empty, long, lat):
    """Create and return a new forest."""
    return Forest(forest_id=forest_id, forest_name=forest_name, region_id=region_id, is_forest_empty=is_forest_empty, long=long, lat=lat)

def create_district(district_id, district_name, region_id, forest_id, is_district_empty, long, lat):
    """Create and return a new district."""
    return District(district_id=district_id, district_name=district_name, region_id=region_id, forest_id=forest_id, is_district_empty=is_district_empty, long=long, lat=lat)

def create_trail(trail_id, trail_no, trail_name, region_id, forest_id, district_id, is_trail_empty, th_long, th_lat):
    """Create and return a new trail."""
    return Trail(trail_id=trail_id, trail_no=trail_no, trail_name=trail_name, region_id=region_id, forest_id=forest_id, district_id=district_id, is_trail_empty=is_trail_empty, th_long=th_long, th_lat=th_lat)

def create_fire(fire_url, fire_name, latitude, longitude, incident_type, last_updated, size, contained, db_updated):
    """Create and return a new fire."""
    return Fire(fire_url=fire_url, fire_name=fire_name, latitude=latitude, longitude=longitude, incident_type=incident_type, last_updated=last_updated, size=size, contained=contained, db_updated=db_updated)


#---------------------------------------------------------------------#
# READ

# Get whole tables
def get_regions():
    """return a list of all Region objects"""
    return Region.query.all()

def get_districts():
    """return a list of all District objects"""
    return District.query.all()

def get_forests():
    """return a list of all Forest objects"""
    return Forest.query.all()

def get_trails():
    """return a list of all Trail objects"""
    return Trail.query.all()

def get_fires():
    """return a list of all Fire objects"""
    return Fire.query.all()

# Get tables by Region

def get_region_by_region(region_id):
    return Region.query.filter_by(region_id = region_id).first()

def get_forests_by_region(region_id):
    return Forest.query.filter_by(region_id = region_id).all()

def get_districts_by_region(region_id):
    return District.query.filter_by(region_id = region_id).all()

def get_trails_by_region(region_id):
    return Trail.query.filter_by(region_id = region_id).all()

# Get tables by Forest

def get_forest_by_forest(forest_id):
    return Forest.query.filter_by(forest_id = forest_id).first()

def get_districts_by_forest(forest_id):
    return District.query.filter_by(forest_id = forest_id).all()

def get_trails_by_forest(forest_id):
    return Trail.query.filter_by(forest_id = forest_id).all()

# Get tables by District

def get_district_by_id(district_id):
    return District.query.filter_by(district_id = district_id).first()

def get_trails_by_district(district_id):
    return Trail.query.filter_by(district_id = district_id).all()

# For calculating distance from trail to fires

def get_fires_with_fire_ids(fires):
    """get list of Fire objects corresponding to list of fire_id numbers"""
    fire_list = []
    for fire in fires:
        fire_list.append(Fire.query.filter(Fire.fire_id == fire.fire_id).one())
    return fire_list

# Miscellaneous
def get_trail_with_trail_name(trail_name):
    """return single Trail instance with trail_name attribute"""
    return Trail.query.filter_by(trail_name = trail_name).one()

def get_trail_with_trail_id(trail_id):
    """return single Trail instance with trail_name attribute"""
    return Trail.query.filter_by(trail_id = trail_id).one()



def get_trail_name_with_trail_id(trail_id):
    return db.session.query(Trail.trail_name).filter(Trail.trail_id == trail_id).first()[0]

def get_trail_ids():
    return [trail[0] for trail in db.session.query(Trail.trail_id).all()]

def get_district_ids():
    return [district[0] for district in db.session.query(District.district_id).all()]

def get_forest_ids():
    return [forest[0] for forest in db.session.query(Forest.forest_id).all()]

def trail_in_district(district):
    return Trail.query.filter_by(district_id = district, is_trail_empty = False).first()

def district_in_forest(forest):
    return District.query.filter_by(forest_id = forest, is_district_empty = False).first()

def district_not_empty(district):
    return District.query.filter_by(district_id = district, is_district_empty = False).first()

def forest_not_empty(forest):
    return Forest.query.filter_by(forest_id = forest, is_forest_empty = False).first()


def get_region_names():
    """return a list of all region names"""
    return [region[0] for region in db.session.query(Region.region_name).all()]

def get_last_db_update():
    return db.session.query(Fire.db_updated).order_by(Fire.db_updated.desc()).first()[0]


#---------------------------------------------------------------------#
# UPDATE

def update_fires():
    

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
    print(f'******* FIRE TABLE UPDATED *******')

    
def set_districts_to_empty():
    """set districts containing only empty trails to empty"""
    districts = get_district_ids()
    for district in districts[:]:
        if trail_in_district(district):
            continue
        else:
            db.session.query(District).filter(District.district_id == district).update(
                {"is_district_empty": True}, synchronize_session="fetch")
            print(district, db.session.query(District.is_district_empty).filter(District.district_id == district).first())
    db.session.commit()
    print(f'******* DISTRICTS TABLE UPDATED *******')

def set_forests_to_empty():
    """set forests containing only empty districts to empty"""
    forests = get_forest_ids()
    for forest in forests[:]:
        if district_in_forest(forest):
            continue
        else:
            db.session.query(Forest).filter(Forest.forest_id == forest).update(
                {"is_forest_empty": True}, synchronize_session="fetch")
            print(forest, db.session.query(Forest.is_forest_empty).filter(Forest.forest_id == forest).first())
    db.session.commit()
    print(f'******* FORESTS TABLE UPDATED *******')


#---------------------------------------------------------------------#

# Connect to database when running crud.py interactively
if __name__ == '__main__':
    from server import app
    connect_to_db(app)
