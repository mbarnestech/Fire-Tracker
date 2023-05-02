# import Python modules
from dotenv import load_dotenv
from flask import Flask, render_template, session, request, jsonify
import jinja2
from os import environ


# import local modules
import crud
import fs_data
import helper
from model import connect_to_db, db

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
    
    today = helper.get_today()
    next_year = helper.get_next_year()

    return render_template("index.html", today = today, next_year = next_year)


@app.route("/initialize")
def initialize_main():
    """populate initial data"""

    index_dict = helper.generate_index_dict()
    print('INITIALIZING' + '*' * 20)
    return jsonify(index_dict)


@app.route('/region')
def set_region():

    region_id = request.args.get('region')
    region_dict = helper.generate_region_dict(region_id)
    print('SETTING REGION' + '*' * 20)
    return jsonify(region_dict)


@app.route('/forest')
def set_forest():

    forest_id = request.args.get('forest')
    forest_dict = helper.generate_forest_dict(forest_id)
    print(f'{forest_dict=}')
    print('SETTING FOREST' + '*' * 20)
    return jsonify(forest_dict)


@app.route('/district')
def set_district():

    district_id = request.args.get('district')
    district_dict = helper.generate_district_dict(district_id)

    return jsonify(district_dict)

@app.route('/trail')
def set_trail():

    trail_id = request.args.get('trail')
    openweatherkey = environ['OPENWEATHERAPIKEY']
    trail_dict = helper.generate_trail_dict(trail_id, openweatherkey)

    return jsonify(trail_dict)

@app.route("/search", methods=['POST'])
def search():

    # get list of TrailPoint objects corresponding to chosen trail
    trail_id = request.form.get('trail-choice')
    trail_name = crud.get_trail_name_with_trail_id(trail_id)
    trailpoint_list = crud.get_trailpoint_list_with_trail_id(trail_id)

    # get requested distance from trail in miles
    miles = request.form.get('fire-distance')
    miles = helper.to_int(miles)
    # get list of Fire instances of nearby fires
    nearby_fires = helper.get_nearby_fires(trailpoint_list, miles)
    
    # add fire information to session
    session['fires'] = [[fire.fire_id, fire.fire_name, fire.longitude, fire.latitude] for fire in nearby_fires]
    return render_template("map.html", fires=nearby_fires, trail_name=trail_name)

@app.route('/initializeMap')
def initialize_map():
    dataForMap = {'mapKey': environ['DEFAULTMAPBOXTOKEN']}
    return jsonify(dataForMap)

@app.route('/regions.geojson')
def publish_geojson_regions():
    region_json = fs_data.get_geojson(fs_data.region_file)
    return region_json

@app.route('/forests.geojson')
def publish_geojson_forests():
    region_id = request.args.get('region')
    forest_json = fs_data.get_forests_geojson_for_region(region_id=region_id)
    print(f'*************{region_id=}, {forest_json.keys=}')
    return forest_json

@app.route('/districts.geojson')
def publish_geojson_districts():
    # TODO only get district info that corresponds to given forest 
    district_json = fs_data.get_geojson(fs_data.district_file)
    return district_json

@app.route('/trails.geojson')
def publish_geojson_trails():
    # TODO only get forest info that corresponds to given trails 
    trail_json = fs_data.get_geojson(fs_data.trail_file)
    return trail_json

@app.route('/trail.geojson')
def publish_single_geojson_trail():
    ## TODO filter out geojson data to only return the trail I want
    trail_json = fs_data.get_geojson(fs_data.trail_file)
    return trail_json


#---------------------------------------------------------------------#

# when this file is run
if __name__ == "__main__":
    # connect to database
    connect_to_db(app)
    # run server
    app.run(debug=True, host="0.0.0.0")