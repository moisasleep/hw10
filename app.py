# This application provides climate data from Hawaii.

# Import dependencies
import sqlalchemy as db
from flask import Flask, jsonify
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

# Create a Flask application
app = Flask(__name__)

# Database Setup
engine = db.create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Define Flask routes
@app.route("/")
def main():
    """Welcome message and available routes."""
    return (
        "Welcome to the Climate App Home Page!<br>"
        "Available Routes:<br>"
        "/api/v1.0/precipitation<br>"
        "/api/v1.0/stations<br>"
        "/api/v1.0/tobs<br>"
        "/api/v1.0/<start><br>"
        "/api/v1.0/<start>/<end><br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Retrieve precipitation data for the last year."""
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).order_by(Measurement.date).all()
    precipitation_dict = {date: prcp for date, prcp in results}
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Retrieve station information."""
    station_info = session.query(Measurement.station).\
        group_by(Measurement.station).all()
    stations_list = [station[0] for station in station_info]
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Retrieve temperature observations for the last year."""
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= prev_year).order_by(Measurement.date).all()
    tobs_dict = {date: tobs for date, tobs in results}
    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")
def start(start):
    """Retrieve temperature data from a given start date."""
    results = session.query(db.func.min(Measurement.tobs), db.func.avg(Measurement.tobs),
                            db.func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    temp_stats = [{"Min": min_temp, "Average": avg_temp, "Max": max_temp} for min_temp, avg_temp, max_temp in results]
    return jsonify(temp_stats)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Retrieve temperature data within a given date range."""
    results = session.query(db.func.min(Measurement.tobs), db.func.avg(Measurement.tobs),
                            db.func.max(Measurement.tobs)).filter(Measurement.date >= start).\
                            filter(Measurement.date <= end).all()
    temp_stats = [{"Min": min_temp, "Average": avg_temp, "Max": max_temp} for min_temp, avg_temp, max_temp in results]
    return jsonify(temp_stats)

if __name__ == "__main__":
    app.run(debug=True) 
