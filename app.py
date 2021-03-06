# Docs on session basics
# https://docs.sqlalchemy.org/en/13/orm/session_basics.html

import numpy as np
import os
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
        f"Available Routes:<br>"
        f"<em>Please enter dates as yyyy-mm-dd</em><br><br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/stations_mostactive<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/START_DATE<br>"
        f"/api/v1.0/START_DATE/END_DATE<br>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a dictionary of all precipitation data"""

    # Query all measurements
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
    """Return a list of all stations"""

    # Query all stations
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

@app.route("/api/v1.0/stations_mostactive")
def stations_mostactive():
    """Return a list of all stations"""

    # Query all stations
    session = Session(engine)
    most_active = session.query(Measurement.station, func.count(Measurement.station)\
        .label('total')).group_by(Measurement.station).order_by(func.count(Measurement.station).label('total').desc()).all()

    # close the session to end the communication with the database
    session.close()
    
    all_stations = []
    for station in most_active:
        station_dict = {}
        station_dict["Name"] = station.station
        station_dict["Record Count"] = station.total
        all_stations.append(station_dict)

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all temperature observations"""

    # Query the data
    session = Session(engine)

    maxdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    max_date = dt.datetime.strptime(maxdate[0], '%Y-%m-%d').date()
    
    query_date = max_date - dt.timedelta(days=365)

    most_active = session.query(Measurement.station, func.count(Measurement.station)\
        .label('total')).group_by(Measurement.station).order_by(func.count(Measurement.station).label('total').desc()).first()

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active[0]).\
        filter(Measurement.date >= query_date)

    # close the session to end the communication with the database
    session.close()
    
    all_temps = []
    for temp in results:
        temp_dict = {}
        temp_dict["date"] = temp.date
        temp_dict["tobs"] = temp.tobs
        all_temps.append(temp_dict)
                
    return jsonify(all_temps)


@app.route("/api/v1.0/<start>")
def start(start):
    """Return a list of all temperature observations"""
        
    # Query the data
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    # close the session to end the communication with the database
    session.close()

    all_temps = []
    temp_dict = {}
    temp_dict['TMIN'] = results[0][0]
    temp_dict['TAVG'] = results[0][1]
    temp_dict['TMAX'] = results[0][2]
    all_temps.append(temp_dict)

    return jsonify(all_temps)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Return a list of all temperature observations"""
        
    # Query the data
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # close the session to end the communication with the database
    session.close()

    all_temps = []
    temp_dict = {}
    temp_dict['TMIN'] = results[0][0]
    temp_dict['TAVG'] = results[0][1]
    temp_dict['TMAX'] = results[0][2]
    all_temps.append(temp_dict)

    return jsonify(all_temps)


if __name__ == '__main__':
    app.run(debug=True)
