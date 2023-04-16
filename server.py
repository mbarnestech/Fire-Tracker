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

# Make undefined variables throw an error in Jinja
app.jinja_env.undefined = jinja2.StrictUndefined

# Make the Flask interactive debugger better in testing 
# TODO - remove before deployment
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


#---------------------------------------------------------------------#

@app.route("/")
def index():
    """Return index."""

    regions = crud.get_region_names()

    return render_template("index.html", regions=regions)

@app.route('/choose_region', methods=['POST'])
def forest():
    """Return forest form."""

    region_name = request.form.get('region-choice')
    forests = crud.get_forests_by_region_name(region_name)

    return render_template("forest.html", region_name = region_name, forests=forests)

@app.route('/choose_forest', methods=['POST'])
def district():
    """Return district form."""

    forest_name = request.form.get('forest-choice')
    districts = crud.get_districts_by_forest_name(forest_name)

    return render_template("district.html", forest_name = forest_name, districts=districts)

@app.route('/choose_district', methods=['POST'])
def trail():
    """Return trail form."""

    district_name = request.form.get('district-choice')
    trails = crud.get_trails_by_district_name(district_name)

    return render_template("trail.html", district_name = district_name, trails=trails)

@app.route("/choose_trail", methods=['POST'])
def choose_trail():
    trail_name = request.form.get('trail-choice')
    session['trail_name'] = trail_name
    return render_template("distance.html", trail_name = trail_name)

@app.route("/choose_distance", methods=['POST'])
def choose_distance():
    trail = crud.get_trail_with_trail_name(session['trail_name'])
    session['trail_id'] = trail.trail_id
    session['miles'] = request.form.get('fire-distance')
   
    # get list of TrailPoint objects corresponding to session trail_id
    trailpoint_list = crud.get_trailpoint_list_with_trail_id(session['trail_id'])
    # add list of [long, lat] pairs to session 
    session['lnglat_list'] = helper.get_lnglat_list(trailpoint_list)

    # get requested distance from trail in miles
    miles = helper.to_int(session['miles'])

    # get list of Fire instances of nearby fires
    nearby_fires = helper.get_nearby_fires(trailpoint_list, miles)
    
    # add fire information to session
    session['fires'] = [[fire.fire_id, fire.fire_name, fire.longitude, fire.latitude] for fire in nearby_fires]

    print(f"{session['trail_name']=}, {session['trail_id']=}, {session['miles']=}, {trailpoint_list=}, {session['fires']=}")

    return render_template("map.html", fires=nearby_fires)

@app.route('/testData')
def giveMapBoxMapData():
    # struggling with how to route to .png image
    dataForMap = {'lngLatList': session['lnglat_list'], 'fires': session['fires'], 'mapKey': environ['DEFAULTMAPBOXTOKEN']}
    return jsonify(dataForMap)


#---------------------------------------------------------------------#

# when this file is run
if __name__ == "__main__":
    # connect to database
    connect_to_db(app)
    # run server
    app.run(debug=True, host="0.0.0.0")