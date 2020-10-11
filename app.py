# Docs on session basics
# https://docs.sqlalchemy.org/en/13/orm/session_basics.html

import numpy as np
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end><br>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all passenger names"""

    # Query all passengers
    session = Session(engine)
    results = session.query(Measurement).all()

    # close the session to end the communication with the database
    session.close()
    
    measurement_dict = {}
    for measurement in results:
        measurement_dict.update({measurement.date:measurement.prcp})
        
    return jsonify(measurement_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all passenger names"""

    # Query all passengers
    session = Session(engine)
    results = session.query(Station).all()

    # close the session to end the communication with the database
    session.close()
    
    all_stations = []
    for station in results:
        station_dict = {}
        station_dict["id"] = station.id
        station_dict["name"] = station.name
        all_stations.append(station_dict)
        
        
    return jsonify(all_stations)


if __name__ == '__main__':
    app.run(debug=True)
