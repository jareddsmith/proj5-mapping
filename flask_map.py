"""
Project 5: Mapping
Made by Jared Smith
"""

import flask
from flask import request
from flask import url_for
from flask import render_template

import json
import logging

###
# Globals
###
app = flask.Flask(__name__)
import CONFIG

import uuid
app.secret_key = str(uuid.uuid4())
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)


###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")

    file = open("poi.txt")
    
    locations = []
    
    for location in file:
        loc = location.split(",")
        loc[1] = float(loc[1])
        loc[2] = float(loc[2])
        
        locations.append(loc)
    
    #Locations are nested in arrays
    #i.e. locations[0][i] (locations[location][data])

    flask.session['locations'] = locations
    
    return flask.render_template('mapping.html')

###################
#   Error handlers
###################
@app.errorhandler(404)
def error_404(e):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return render_template('404.html'), 404

###############
# Set up to run from cgi-bin script, from
# gunicorn, or stand-alone.
#

if __name__ == "__main__":
    # Standalone.
    app.debug = True
    app.logger.setLevel(logging.DEBUG)
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
else:
    # Running from cgi-bin or from gunicorn WSGI server,
    # which makes the call to app.run.  Gunicorn may invoke more than
    # one instance for concurrent service.
    app.secret_key = CONFIG.secret_key
    app.debug=False
