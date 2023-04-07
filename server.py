# import Python modules
from flask import Flask, render_template, redirect, flash, session, request, jsonify
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
    trails = crud.get_trails()
    return render_template("index.html", trails=trails)

@app.route("/choose_trail", methods=['POST'])
def choose_trail():
    """Set session trail information"""
    session['trail_name'] = request.json.get('trailChoice')
    print(f"*********** {session['trail_name']=} ***********")
    trail = crud.get_trail_with_trail_name(session['trail_name'])

    session['trail_id'] = trail.trail_id
    print(f"*********** trail id: {session['trail_id']=}")
    # get list of TrailPoint objects corresponding to session trail_id
    trailpoint_list = crud.get_trailpoint_list_with_trail_id(session['trail_id'])
    print(f'TRAILPOINTS = {trailpoint_list=}')
    # get requested distance from trail in miles
    miles = helper.to_int(request.args.get('miles'))

    # get list of Fire instances of nearby fires
    nearby_fires = helper.get_nearby_fires(trailpoint_list, miles)
    print(f'NEARBY FIRES CHECK: {nearby_fires}')
    session['fires'] = []
    print(f"*********** first: {session['fires']=}")
    fire_dict = {}
    for fire in nearby_fires:
        fire_dict[fire.fire_name] = fire_dict.get(fire.fire_name, fire.fire_url)
    # add fire information to session
    session['fires'] = [fire.fire_id for fire in nearby_fires]
    print(f"*********** second: {session['fires']=}")

    return jsonify(fire_dict)

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