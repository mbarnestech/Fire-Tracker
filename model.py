#import Python modules
from flask_sqlalchemy import SQLAlchemy

#---------------------------------------------------------------------#

# create db instance from SQLAlchemy
db = SQLAlchemy()

#---------------------------------------------------------------------#
# NOTE look for cronjob for timing inciweb scraping

class Region(db.Model):
    """A US Forest Service Region
    
    Data from https://data-usfs.hub.arcgis.com/
    Forest Service Regional Boundaries (Feature Layer).
    """

    __tablename__ = 'regions'

    region_id = db.Column(db.String, primary_key=True)
    region_name = db.Column(db.String, nullable = False)

    forests = db.relationship('Forest', back_populates='region')
    districts = db.relationship('District', back_populates='region')
    trails = db.relationship('Trail', back_populates='region')
    region_coords = db.relationship('RegionCoord', back_populates='region')

    def __repr__(self):
        return f'<Region id={self.region_id} name={self.region_name}>'

class RegionCoord(db.Model):
    """Coordinates for a USFS Region"""

    __tablename__ = 'region_coords'

    coord_id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.String, db.ForeignKey('regions.region_id'))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    region = db.relationship('Region', back_populates='region_coords')

    def __repr__(self):
        return f'<RegionCoord id={self.coord_id} region name={self.region_name}>'

class Forest(db.Model):
    """A US Forest Service National Forest
    
    Data from https://data-usfs.hub.arcgis.com/
    Forest Administrative Boundaries (Feature Layer).
    """

    __tablename__ = 'forests'

    forest_id = db.Column(db.String, primary_key=True)
    region_id = db.Column(db.String, db.ForeignKey('regions.region_id'))
    forest_name = db.Column(db.String, nullable = False)
    is_forest_empty = db.Column(db.Boolean, nullable = False)

    region = db.relationship('Region', back_populates='forests')
    districts = db.relationship('District', back_populates='forest')
    trails = db.relationship('Trail', back_populates='forest')
    forest_coords = db.relationship('ForestCoord', back_populates='forest')

    def __repr__(self):
        return f'<Forest id={self.forest_id} name={self.forest_name}>'
    

class ForestCoord(db.Model):
    """Coordinates for a USFS Forest"""

    __tablename__ = 'forest_coords'

    coord_id = db.Column(db.Integer, primary_key=True)
    forest_id = db.Column(db.String, db.ForeignKey('forests.forest_id'))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    forest = db.relationship('Forest', back_populates='forest_coords')

    def __repr__(self):
        return f'<ForestCoord id={self.coord_id} forest id={self.forest_id}>'


class District(db.Model):
    """A US Forest Service National Forest Ranger District
    
    Data from https://data-usfs.hub.arcgis.com/
    Forest Administrative Boundaries (Feature Layer).
    """

    __tablename__ = 'districts'

    district_id = db.Column(db.String, primary_key=True) 
    region_id = db.Column(db.String, db.ForeignKey('regions.region_id'))  
    forest_id = db.Column(db.String, db.ForeignKey('forests.forest_id')) 
    district_name = db.Column(db.String, nullable = False)
    is_district_empty = db.Column(db.Boolean, nullable = False)

    region = db.relationship('Region', back_populates='districts')
    forest = db.relationship('Forest', back_populates='districts')
    trails = db.relationship('Trail', back_populates='district')
    district_coords = db.relationship('DistrictCoord', back_populates='district')

    def __repr__(self):
        return f'<District id={self.district_id} name={self.district_name}>'


class DistrictCoord(db.Model):
    """Coordinates for a USFS District"""

    __tablename__ = 'district_coords'

    coord_id = db.Column(db.Integer, primary_key=True)
    district_id = db.Column(db.String, db.ForeignKey('districts.district_id'))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    district = db.relationship('District', back_populates='district_coords')

    def __repr__(self):
        return f'<DistrictCoord id={self.coord_id} district id={self.district_id}>'
    

class Trail(db.Model):
    """A US Forest Service National Forest Trail
    
    Data from https://data-usfs.hub.arcgis.com/
    National Forest System Trails (Feature Layer)    
    """

    __tablename__ = 'trails'

    trail_id = db.Column(db.String, primary_key=True)
    trail_no = db.Column(db.String, nullable=False)
    trail_name = db.Column(db.String, nullable=False)
    region_id = db.Column(db.String, db.ForeignKey('regions.region_id'))  
    forest_id = db.Column(db.String, db.ForeignKey('forests.forest_id'))  
    district_id = db.Column(db.String, db.ForeignKey('districts.district_id'))
    is_trail_empty = db.Column(db.Boolean, nullable = False)  

    trail_points = db.relationship('TrailPoint', back_populates='trail')
    region = db.relationship('Region', back_populates='trails')
    forest = db.relationship('Forest', back_populates='trails')
    district = db.relationship('District', back_populates='trails')
       
    def __repr__(self):
        return f'<Trail id={self.trail_id} name={self.trail_name}>'


class TrailPoint(db.Model):
    """Lat/Long points for each trail"""

    __tablename__ = 'trail_points'
    
    trail_point_id = db.Column(db.Integer, primary_key=True)
    trail_id = db.Column(db.String, db.ForeignKey('trails.trail_id'))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    trail = db.relationship('Trail', back_populates='trail_points')

    def __repr__(self):
        return f'<TrailPoint id={self.trail_point_id} trail={self.trail_id}>'
    

class Fire(db.Model):
    """A fire
    
    Data from inciweb.wildfire.gov."""

    __tablename__ = 'fires'

    fire_id = db.Column(db.Integer, primary_key=True)
    fire_url = db.Column(db.String, unique=True, nullable=False)
    fire_name = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    incident_type = db.Column(db.String)
    last_updated = db.Column(db.String)
    size = db.Column(db.Integer)
    contained = db.Column(db.Integer)
    db_updated = db.Column(db.String)
       
    def __repr__(self):
        return f'<Fire id={self.fire_id} name={self.fire_name}>'
    

#---------------------------------------------------------------------#

# connect to database
def connect_to_db(flask_app, db_uri="postgresql:///fire_tracker", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

# if model.py is being run directly
if __name__ == "__main__":
    # get Flask app
    from server import app

    # Connects to db to flask server, makes FlaskSQLALchemy work.
    # Change to connect_to_db(app, echo=False) to not see all the printed queries
    connect_to_db(app)
