# import Python modules
from flask import Flask, render_template, redirect, flash, session, request
import jinja2

# import local modules
from model import connect_to_db, db, Trail, TrailPoint, Fire

#---------------------------------------------------------------------#

# create Flask app
app = Flask(__name__)

# Create secret key to use Flask session feature TODO - bring this in from a secrets file instead before deployment
app.secret_key = 'I AM NOT A SECRET KEY YET; ANYONE CAN SEE ME ON GITHUB'

# Make undefined variables throw an error in Jinja
app.jinja_env.undefined = jinja2.StrictUndefined

# Make the Flask interactive debugger better in testing 
# TODO - remove before deployment
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True

#---------------------------------------------------------------------#

@app.route("/")
def index():
    """Return index."""
    trails = Trail.query.all()
    return render_template("index.html", trails=trails)

@app.route("/choose_trail")
def choose_trail():
    """Show chosen trail, ask for distance to check for fires"""
    session['trail_name'] = request.args.get('trail-choice')

    trail = Trail.query.filter_by(trail_name = session['trail_name']).one()
    session['trail_id'] = trail.trail_id

    return render_template('trail_choice.html')

@app.route("/fire_check")
def check_for_fire():
    """Show whether fires exist within distance from trail"""

    # get object for chosen trail
    # trail_object = Trail.query.filter_by(trail_id = session['trail_id']).one()
    # get list of trailpoints for chosen trail
    trailpoint_list = db.session.query(TrailPoint).filter(Trail.trail_id == session['trail_id']).all()
    
    # create function to get the maximum and minimum latitude and longitude of the trail
    def get_maxmin_latlong(points):
        max_lat = points[0].latitude
        min_lat = max_lat
        max_long = points[0].longitude
        min_long = max_long
        for point in points:
            if point.latitude > max_lat:
                max_lat = point.latitude
            elif point.latitude < min_lat:
                min_lat = point.latitude
            if point.longitude > max_long:
                max_long = point.longitude
            elif point.longitude < min_long:
                min_long = point.longitude
        return (min_lat, max_lat, min_long, max_long)
    
    # create variables for maximum and minimum longitude of the trail
    min_lat, max_lat, min_long, max_long = get_maxmin_latlong(trailpoint_list)

    # get a list of fires
    fires = Fire.query.all()

    # get set distance from trail (temporarily hardcoding 50 miles)
    miles = int(request.args.get('fire-distance'))

    # use 1 deg latitude = 69 miles and 1 deg longitude = 54.6 miles to get radius in lat/long
        # this is math based on numbers from 38 deg North latitude, which I'm calling close enough for my purposes here
    lat_offset = miles/69
    long_offset = miles/54.6

    # create min/max lat/long boundaries for fire search
    min_lat -= lat_offset
    max_lat += lat_offset
    min_long -= long_offset
    max_long += long_offset

    nearby_fires = []
    session['fires'] = []
    # check for fires within range of offset
    for fire in fires:
        if min_lat < fire.latitude < max_lat and min_long < fire.longitude < max_long:
            nearby_fires.append(fire)
            

    return render_template('nearby_fires.html', fires = nearby_fires)

@app.route('/go_to_map')
def go_to_map():
    """Return map of trail and nearby fires"""

    trailhead = db.session.query(TrailPoint).filter(Trail.trail_id == session['trail_id']).first()

    return render_template('map.html', trailhead = trailhead)


#---------------------------------------------------------------------#

# when this file is run
if __name__ == "__main__":
    # connect to database
    connect_to_db(app)
    # run server
    app.run(debug=True, host="0.0.0.0")