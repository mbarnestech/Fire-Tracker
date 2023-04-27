"""CRUD functions live here"""

# import local modules
from model import Region, Forest, District, Trail, TrailPoint, Fire, RegionCoord, ForestCoord, DistrictCoord,db, connect_to_db
import helper
import fire_data


#---------------------------------------------------------------------#
# CREATE

def create_region(region_id, region_name):
    """Create and return a new region."""
    return Region(region_id=region_id, region_name=region_name)

def create_region_coords(region_id, latitude, longitude):
    """Create and return a new region coordinate"""
    return RegionCoord(region_id=region_id, latitude=latitude, longitude=longitude)

def create_forest(forest_id, forest_name, region_id):
    """Create and return a new forest."""
    return Forest(forest_id=forest_id, forest_name=forest_name, region_id=region_id)

def create_forest_coords(forest_id, polygon_no, latitude, longitude):
    """Create and return a new forest coordinate"""
    return ForestCoord(forest_id=forest_id, polygon_no=polygon_no, latitude=latitude, longitude=longitude)

def create_district(district_id, district_name, region_id, forest_id):
    """Create and return a new district."""
    return District(district_id=district_id, district_name=district_name, region_id=region_id, forest_id=forest_id)

def create_district_coords(district_id, polygon_no, latitude, longitude):
    """Create and return a new district coordinate"""
    return DistrictCoord(district_id=district_id, polygon_no=polygon_no, latitude=latitude, longitude=longitude)

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

# Get whole tables
def get_regions():
    """return a list of all Region objects"""
    return Region.query.all()

def get_region_coords():
    """return a list of all RegionCoord objects"""
    return RegionCoord.query.all()

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

def get_forests_by_region(region_name):
    return Forest.query.join(Region).filter_by(region_name = region_name).all()

def get_districts_by_region(region_name):
    return District.query.join(Region).filter_by(region_name = region_name).all()

def get_trails_by_region(region_name):
    return Trail.query.join(Region).filter_by(region_name = region_name).all()

# Get tables by Forest

def get_districts_by_forest(forest_name):
    return District.query.join(Forest).filter_by(forest_name = forest_name).all()

def get_trails_by_forest(forest_name):
    return Trail.query.join(Forest).filter_by(forest_name = forest_name).all()

# Get tables by District

def get_trails_by_district(district_name):
    return Trail.query.join(District).filter_by(district_name = district_name).all()

# For calculating distance from trail to fires

def get_trailpoint_list_with_trail_id(trail_id):
    """return a list of TrailPoint objects corresponding to a trail name"""
    return TrailPoint.query.filter_by(trail_id = trail_id).all()

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

def get_trail_name_with_trail_id(trail_id):
    return db.session.query(Trail.trail_name).filter(Trail.trail_id == trail_id).first()[0]

def get_trail_ids():
    return [trail[0] for trail in db.session.query(Trail.trail_id).all()]

def get_district_ids():
    return [district[0] for district in db.session.query(District.district_id).all()]

def get_forest_ids():
    return [forest[0] for forest in db.session.query(Forest.forest_id).all()]

def trailpoint_in_trail(trail_id):
    return TrailPoint.query.filter_by(trail_id = trail_id).first()

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
    print(f'******* FIRE TABLE UPDATED *******')
    
def set_trails_to_empty():
    """set trails with no associated trailpoints to empty"""
    trails = get_trail_ids()
    for trail in trails[:]:
        if trailpoint_in_trail(trail):
            continue
        else:
            db.session.query(Trail).filter(Trail.trail_id == trail).update(
                {"is_trail_empty": True}, synchronize_session="fetch")
            print(trail, db.session.query(Trail.is_trail_empty).filter(Trail.trail_id == trail).first())
    db.session.commit()
    print(f'******* TRAILS TABLE UPDATED *******')
    
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
