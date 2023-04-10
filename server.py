# import Python modules
from flask import Flask, render_template, redirect, flash, session, request, jsonify
from dotenv import load_dotenv
from os import environ
import jinja2

# import local modules
from model import connect_to_db, db
import crud
import helper

#---------------------------------------------------------------------#

# create Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()

# Create secret key to use Flask session feature
app.secret_key = environ['APPSECRETKEY']
print(f'********{app.secret_key=}')

# Make undefined variables throw an error in Jinja
app.jinja_env.undefined = jinja2.StrictUndefined

# Make the Flask interactive debugger better in testing 
# TODO - remove before deployment
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


#---------------------------------------------------------------------#

@app.route("/")
def index():
    """Return index."""
    trails = crud.get_trails()
    return render_template("index.html", trails=trails)

@app.route("/choose_trail", methods=['POST'])
def choose_trail():
    """Set session trail information"""
    session['trail_name'] = request.form.get('trail-choice')
    trail = crud.get_trail_with_trail_name(session['trail_name'])
    session['trail_id'] = trail.trail_id
    session['miles'] = request.form.get('fire-distance')
   
    # get list of TrailPoint objects corresponding to session trail_id
    trailpoint_list = crud.get_trailpoint_list_with_trail_id(session['trail_id'])
    trailhead = trailpoint_list[0]
    session['th_lat'] = trailhead.latitude
    session['th_lng'] = trailhead.longitude
    print(f"********** {session['th_lat']=}, {session['th_lng']=}")
    # get requested distance from trail in miles
    miles = helper.to_int(session['miles'])

    # get list of Fire instances of nearby fires
    nearby_fires = helper.get_nearby_fires(trailpoint_list, miles)
    
    # add fire information to session
    session['fires'] = [fire.fire_id for fire in nearby_fires]

    print(f"{session['trail_name']=}, {session['trail_id']=}, {session['miles']=}, {trailpoint_list=}, {session['fires']=}")

    return render_template("map.html", fires=nearby_fires, th_lat = session['th_lat'], th_lng = session['th_lng'])

@app.route('/testData')
def giveMapBoxMapData():
    dataForMap = {'thLat': session['th_lat'], 'thLng': session['th_lng'], 'mapKey': environ['DEFAULTMAPBOXTOKEN']}
    return jsonify(dataForMap)

@app.route('/go_to_map')
def go_to_map():
    """Return map of trail and nearby fires"""
    trail = crud.get_trail_with_trail_name(session['trail_name'])
    fires = crud.get_fires_with_fire_ids(session['fires'])
    return render_template('map.html', trail=trail, fires = fires)


#---------------------------------------------------------------------#

# when this file is run
if __name__ == "__main__":
    # connect to database
    connect_to_db(app)
    # run server
    app.run(debug=True, host="0.0.0.0")