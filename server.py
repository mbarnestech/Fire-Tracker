# import Python modules
from flask import Flask, render_template, redirect, flash, session, request
import jinja2

# import local modules
from model import connect_to_db, db, Trail, TrailPoint, Fire
import crud
import helper

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

    # get list of TrailPoint objects corresponding to session trail_id
    trailpoint_list = crud.get_trailpoint_list_with_trail_id(session['trail_id'])

    # get requested distance from trail in miles
    miles = helper.to_int(request.args.get('fire-distance'))

    # get list of Fire instances of nearby fires
    nearby_fires = helper.get_nearby_fires(trailpoint_list, miles)

    return render_template('nearby_fires.html', fires = nearby_fires)

@app.route('/go_to_map')
def go_to_map():
    """Return map of trail and nearby fires"""

    return render_template('map.html')


#---------------------------------------------------------------------#

# when this file is run
if __name__ == "__main__":
    # connect to database
    connect_to_db(app)
    # run server
    app.run(debug=True, host="0.0.0.0")