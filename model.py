#import Python modules
from flask_sqlalchemy import SQLAlchemy

# create db instance from SQLALchemy
db = SQLAlchemy()

# create classes for each table

class Trail(db.Model):
    """A trail, data from HikingProject.com."""

    __tablename__ = 'trails'

    trail_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    trail_url = db.Column(db.String, unique=True, nullable=False)
    gpx_url = db.Column(db.String, unique=True, nullable=False)
    miles = db.Column(db.Float)
    kilometers = db.Column(db.Float)
    high_elevation = db.Column(db.Integer)
    low_elevation = db.Column(db.Integer)
    total_elevation_gain = db.Column(db.Integer)
    trail_type = db.Column(db.String)
    difficulty = db.Column(db.String)
    last_condition = db.Column(db.String)
    last_condition_update = db.Column(db.Date)
    last_condition_notes = db.Column(db.String)
    stars = db.Column(db.Float)
    state = db.Column(db.String)
    area = db.Column(db.String)
    subarea = db.Column(db.String)
    city = db.Column(db.String)

    trail_points = db.relationship('TrailPoint', back_populates='trail')
       
    def __repr__(self):
        return f'<Trail id={self.trail_id} email={self.email}>'


class TrailPoint(db.Model):
    """Lat/Long points for each trail"""

    __tablename__ = 'trail_points'
    
    trail_point_id = db.Column(db.Integer, primary_key=True)
    trail_id = db.Column(db.Integer, db.ForeignKey('Trail.trail_id'))
    latitude = db.Column(db.String)
    longitude = db.Column(db.String)
    elevation = db.Column(db.Float)

    trail = db.relationship('Trail', back_populates='trail_points')

    def __repr__(self):
        return f'<TrailPoint id={self.trail_point_id} trail={self.trail_id}>'
    

class Fire(db.Model):
    """A fire, data from inciweb.wildfire.gov."""

    __tablename__ = 'fires'

    fire_id = db.Column(db.Integer, primary_key=True)
    fire_url = db.Column(db.String, unique=True, nullable=False)
    fire_name = db.Column(db.String, nullable=False)
    latitude = db.Column(db.String, nullable=False)
    longitude = db.Column(db.String, nullable=False)
    incident_type = db.Column(db.String)
    last_updated = db.Column(db.Date)
    size = db.Column(db.Integer)
    contained = db.Column(db.Integer)
       
    def __repr__(self):
        return f'<Fire id={self.fire_id} name={self.fire_name}>'
    

# need to name psql database & replace <##########>
def connect_to_db(flask_app, db_uri="postgresql:///<##########>", echo=True):
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
