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

    if helper.fires_are_old():
        crud.update_fires()
    else:
        print('+++++++++++ NO UPDATE NEEDED +++++++++++')

    return render_template("index.html")


@app.route("/initialize")
def initialize_main():
    """populate initial data"""

    index_dict = helper.generate_index_dict()
    print('INITIALIZING' + '*' * 20)
    return jsonify(index_dict)


@app.route('/region')
def set_region():

    region_name = request.args.get('region')
    region_dict = helper.generate_region_dict(region_name)
    print('SETTING REGION' + '*' * 20)
    return jsonify(region_dict)


@app.route('/forest')
def set_forest():

    forest_name = request.args.get('forest')
    forest_dict = helper.generate_forest_dict(forest_name)
    print('SETTING FOREST' + '*' * 20)
    print(forest_name, forest_dict)
    return jsonify(forest_dict)


@app.route('/district')
def set_district():

    district_name = request.args.get('district')
    district_dict = helper.generate_district_dict(district_name)

    return jsonify(district_dict)


@app.route("/choose_distance", methods=['POST'])
def choose_distance():

    # get list of TrailPoint objects corresponding to chosen trail
    trail_name = request.form.get('trail-choice')
    trailpoint_list = crud.get_trailpoint_list_with_trail_name(trail_name)
    # get list of lats and longs from 
    session['lnglat_list'] = helper.get_lnglat_list(trailpoint_list)

    # get requested distance from trail in miles
    miles = request.form.get('fire-distance')
    miles = helper.to_int(miles)

    # get list of Fire instances of nearby fires
    nearby_fires = helper.get_nearby_fires(trailpoint_list, miles)
    
    # add fire information to session
    session['fires'] = [[fire.fire_id, fire.fire_name, fire.longitude, fire.latitude] for fire in nearby_fires]

    return render_template("map.html", fires=nearby_fires, trail_name=trail_name)

@app.route('/mapData')
def giveMapBoxMapData():
    dataForMap = {'lngLatList': session['lnglat_list'], 'fires': session['fires'], 'mapKey': environ['DEFAULTMAPBOXTOKEN']}
    return jsonify(dataForMap)


#---------------------------------------------------------------------#

# when this file is run
if __name__ == "__main__":
    # connect to database
    connect_to_db(app)
    # run server
    app.run(debug=True, host="0.0.0.0")