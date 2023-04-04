#import Python modules
from flask_sqlalchemy import SQLAlchemy


# create db instance from SQLAlchemy
db = SQLAlchemy()

# create classes for each table

class Trail(db.Model):
    """A trail, data from HikingProject.com."""

    __tablename__ = 'trails'

    trail_id = db.Column(db.Integer, primary_key=True)
    trail_name = db.Column(db.String, nullable=False)
    hp_id = db.Column(db.String, unique=True, nullable=False)  
    state = db.Column(db.String)
    area = db.Column(db.String)
    city = db.Column(db.String)

    trail_points = db.relationship('TrailPoint', back_populates='trail')
       
    def __repr__(self):
        return f'<Trail id={self.trail_id} name={self.trail_name}>'


class TrailPoint(db.Model):
    """Lat/Long points for each trail"""

    __tablename__ = 'trail_points'
    
    trail_point_id = db.Column(db.Integer, primary_key=True)
    trail_id = db.Column(db.Integer, db.ForeignKey('trails.trail_id'))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    trail = db.relationship('Trail', back_populates='trail_points')

    def __repr__(self):
        return f'<TrailPoint id={self.trail_point_id} trail={self.trail_id}>'
    

class Fire(db.Model):
    """A fire, data from inciweb.wildfire.gov."""

    __tablename__ = 'fires'

    fire_id = db.Column(db.Integer, primary_key=True)
    fire_url = db.Column(db.String, unique=True, nullable=False)
    fire_name = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    incident_type = db.Column(db.String)
    last_updated = db.Column(db.Date)
    size = db.Column(db.Integer)
    contained = db.Column(db.Integer)
       
    def __repr__(self):
        return f'<Fire id={self.fire_id} name={self.fire_name}>'
    


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
