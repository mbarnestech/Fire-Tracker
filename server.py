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

# Make the openweather key a global variable
openweatherkey = environ['OPENWEATHERAPIKEY']


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
    print(f'{district_dict=}')
    return jsonify(district_dict)

@app.route('/trail')
def set_trail():

    trail_id = request.args.get('trail')
    distance = request.args.get('distance')
    print(f'(((((((((((( {trail_id=}, {distance=}))))))))))))')
    trail_dict = helper.generate_trail_dict(trail_id, openweatherkey, distance)
    print(f'{trail_dict=}')
    return jsonify(trail_dict)

@app.route('/initializeMap')
def initialize_map():
    dataForMap = {'mapKey': environ['DEFAULTMAPBOXTOKEN']}
    return jsonify(dataForMap)

@app.route('/regions.geojson')
def publish_geojson_regions():
    region_json = fs_data.get_geojson(fs_data.region_geojson)
    return region_json

@app.route('/forests.geojson')
def publish_geojson_forests():
    region_id = request.args.get('region')
    forest_json = fs_data.get_forests_geojson_for_region(region_id=region_id)
    print(f'*************{region_id=}, {forest_json.keys=}')
    return forest_json

@app.route('/districts.geojson')
def publish_geojson_districts():
    forest_id = request.args.get('forest')
    district_json = fs_data.get_districts_geojson_for_forest(forest_id=forest_id)
    print(f'*************{forest_id=}, {district_json.keys=}')
    return district_json

@app.route('/trails.geojson')
def publish_geojson_trails():
    district_id = request.args.get('district')
    trails_json = fs_data.get_trails_geojson_for_district(district_id=district_id)
    print(f'*************{district_id=}, {trails_json.keys=}')
    return trails_json

@app.route('/trail.geojson')
def publish_single_geojson_trail():
    trail_id = request.args.get('trail')
    trail_json = fs_data.get_trail(trail_id=trail_id)
    print(f'*************{trail_id=}, {trail_json.keys=}')
    return trail_json

@app.route('/weather')
def get_weather():
    date = request.args.get('date')
    trail_id = request.args.get('trail')
    print(f'%%%%%%%%%%%%{date=}  {trail_id=}')
    weather_dict = helper.get_weather_dict(date, trail_id, openweatherkey)
    return jsonify(weather_dict)

#---------------------------------------------------------------------#

# when this file is run
if __name__ == "__main__":
    # connect to database
    connect_to_db(app)
    # run server
    app.run(debug=True, host="0.0.0.0")