# import Python modules
import os
from datetime import datetime

# import local modules
import crud
import model
import server
import fs_data
import fire_data

#---------------------------------------------------------------------#
def regenerate_db():
    """run to delete fire_tracker db from system and replace with structure from model.py"""

    # delete fire_tracker db if it exists
    os.system('dropdb --if-exists fire_tracker')
    # create new fire_tracker db
    os.system('createdb fire_tracker')
    # with server.app.app_context():
    model.connect_to_db(server.app)
    # add structure to database
    model.db.create_all()

#---------------------------------------------------------------------#

def seed_regions(regions):
    """for a given region, create Region instance and add it to the db session"""
    
    for region in regions:
        if model.Region.query.filter_by(region_id = region['region_id']).first():
            continue
        model.db.session.add(crud.create_region(region['region_id'], 
                                                region['region_name']
                                                ))
        
    model.db.session.commit()


def seed_forests(forests):
    """for a given forest, create Forest instance and add it to the db session"""
    for forest in forests:
        if model.Forest.query.filter_by(forest_id = forest['forest_id']).first():
            continue
        model.db.session.add(crud.create_forest(forest['forest_id'], 
                                                forest['forest_name'],
                                                forest['region_id'],
                                                forest['is_forest_empty']
                                                ))
    model.db.session.commit()


def seed_districts(districts):
    """for a given district, create District instance and add it to the db session"""
    for district in districts:
        if model.District.query.filter_by(district_id = district['district_id']).first():
            continue
        model.db.session.add(crud.create_district(district['district_id'], 
                                                  district['district_name'],
                                                  district['region_id'],
                                                  district['forest_id'],
                                                  district['is_district_empty']
                                                  ))
        
    model.db.session.commit()


def seed_trails(trails):
    """for a given trail, create Trail instance and add it to the db session"""
    
    for trail in trails:
        if (model.Trail.query.filter_by(trail_id = trail['trail_id']).first()
            or not model.District.query.filter_by(district_id = trail['district_id']).first()):
            continue
        model.db.session.add(crud.create_trail(
                                            trail['trail_id'],
                                            trail['trail_no'],
                                            trail['trail_name'], 
                                            trail['region_id'],
                                            trail['forest_id'], 
                                            trail['district_id'],
                                            trail['is_trail_empty']
                                            ))
    # commit to db
    model.db.session.commit()


def seed_trail_points(trail_points):
    """for a given trail point, create TrailPoint instance and add it to the db session"""
    for trail_point in trail_points:
        if model.Trail.query.filter_by(trail_id = trail_point['trail_id']).first():
            model.db.session.add(crud.create_trail_point(trail_point['trail_id'], 
                                        trail_point['latitude'],
                                        trail_point['longitude']
                                        ))
    model.db.session.commit()


def seed_region_coords(region_coords):
    """for a given region, create RegionCoord instance and add it to the db session"""
    for coord in region_coords:
        model.db.session.add(crud.create_region_coords(coord['region_id'], 
                                    coord['latitude'],
                                    coord['longitude']
                                    ))
    model.db.session.commit()


def seed_forest_coords(forest_coords):
    """for a given forest, create ForestCoord instance and add it to the db session"""
    for coord in forest_coords:
        if crud.forest_not_empty(coord['forest_id']):
            model.db.session.add(crud.create_forest_coords(coord['forest_id'], 
                                                           coord['polygon_no'],
                                                           coord['latitude'],
                                                           coord['longitude']
                                                           ))
    model.db.session.commit()


def seed_district_coords(district_coords):
    """for a given district, create DistrictCoord instance and add it to the db session"""
    for coord in district_coords:
        if crud.district_not_empty(coord['district_id']):
            model.db.session.add(crud.create_district_coords(coord['district_id'], 
                                                             coord['polygon_no'],
                                                             coord['latitude'],
                                                             coord['longitude']
                                                             ))
    model.db.session.commit()

def add_coord_tables():
    """add District, Foreign, and Region Coordinate tables to db"""
    model.connect_to_db(server.app)
    model.DistrictCoord.__table__.create(model.db.engine)
    model.ForestCoord.__table__.create(model.db.engine)
    model.RegionCoord.__table__.create(model.db.engine)


def replace_fires_table():
    """replace fires table"""
    model.connect_to_db(server.app)
    model.Fire.__table__.drop(model.db.engine)
    model.Fire.__table__.create(model.db.engine)


def seed_fires(fires):
    """for a given fire, create Fire instance and add it to the db session"""
    for fire in fires:
        model.db.session.add(crud.create_fire(fire['fire_url'],
                                    fire['fire_name'],
                                    fire['latitude'],
                                    fire['longitude'],
                                    fire['incident_type'],
                                    fire['last_updated'],
                                    fire['size'],
                                    fire['contained']
                                    ))
    model.db.session.commit()