import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"/api/v1.0/percipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/2017-08-01<br/>"
        f"/api/v1.0/start/end<br/>"
        f"/api/v1.0/2017-04-01/2017-04-15<br/>"
    )


@app.route("/api/v1.0/percipitation")
def percipitation():
    """Return a list of all passenger names"""
    # Query all passengers
    results = pd.DataFrame(session.query(Measurement.date,func.sum(Measurement.prcp).
        label('total')).filter(Measurement.date > '2016-08-23').group_by(Measurement.date).all())
    # Convert list of tuples into normal list
    percipitation = list(np.ravel(results))
    return jsonify(percipitation)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all passenger names"""
    # Query all passengers
    results = station_df = pd.DataFrame(session.query(Measurement.station,func.count(Measurement.station).
        label('count')).group_by(Measurement.station).order_by('count').all())
    # Convert list of tuples into normal list
    stations = list(np.ravel(results))
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of dates"""
    # Query all passengers
    results = tobs_df = pd.DataFrame(session.query(Measurement.station, Measurement.date,Measurement.tobs.label('temperature')).
        filter(Measurement.date > '2016-08-23').all())
    # Convert list of tuples into normal list
    tobs = list(np.ravel(results))
    return jsonify(tobs)


@app.route("/api/v1.0/<start>")
def start(start):
    sdate = (start)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= sdate).all()
    start = list(np.ravel(results))
    return jsonify(start)

@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    sdate = (start)
    edate = (end)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= sdate,Measurement.date <= edate).all()
    start = list(np.ravel(results))
    return jsonify(start)



if __name__ == '__main__':
    app.run(debug=True)
