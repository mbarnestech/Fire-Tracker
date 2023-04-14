"""SQLAlchemy query functions live here"""

# import local modules
from model import Region, Forest, District, Trail, TrailPoint, Fire, connect_to_db, db

#---------------------------------------------------------------------#

def get_trails():
    """return a list of all Trail objects"""
    return Trail.query.all()


def get_fires():
    """return a list of all Fire objects"""
    return Fire.query.all()


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
    

#---------------------------------------------------------------------#

# Connect to database when running query.py interactively
if __name__ == '__main__':
    from server import app
    connect_to_db(app)
