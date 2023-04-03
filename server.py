# import Python modules
from flask import Flask, render_template, redirect, flash, session
import jinja2

# import local modules
import model

# create Flask app
app = Flask(__name__)

# Create secret key to use Flask session feature TODO - bring this in from a secrets file instead before deployment
app.secret_key = 'I AM NOT A SECRET KEY YET, ANYONE CAN SEE ME ON GITHUB'

# Make undefined variables throw an error in Jinja
app.jinja_env.undefined = jinja2.StrictUndefined

# Make the Flask interactive debugger better in testing 
# ***** REMOVE IN PRODUCTION *****
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True

@app.route("/")
def index():
    """Return index."""

    return render_template("index.html")


# run server when this file is run
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")