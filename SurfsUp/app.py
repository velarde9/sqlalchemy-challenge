# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, MetaData
import numpy as np
from flask import Flask, jsonify
import datetime as dt
from dateutil.relativedelta import relativedelta

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

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
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    year_ago = dt.date(2017, 8 ,23) - relativedelta(years=1)

    precipitation_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).order_by(Measurement.date.asc()).all()
    session.close()

    precipitation_results = []
    for date, precipitation in precipitation_data:
        precipitation_dict = {}
        precipitation_dict[date] = precipitation
        precipitation_results.append(precipitation_dict)
    return jsonify(precipitation_results)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    stations_data = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()

    print(stations_data)
    station_results = []
    for station, name, latitude, longitude, elevation in stations_data:
        station_dict = {}
        station_dict['station'] = station
        station_dict['name'] = name
        station_dict['latitude'] = latitude
        station_dict['longitude'] = longitude
        station_dict['elevation'] = elevation
        station_results.append(station_dict)
    return jsonify(station_results)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    active_stations = session.query(Measurement.station,
    func.count(Measurement.station)).order_by(func.count(Measurement.station).desc()).group_by(Measurement.station).all()
    
    year_ago = dt.date(2017, 8 ,23) - relativedelta(years=1)
    most_active_station_id = active_stations[0][0]
    tobs_hist = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_station_id).filter(Measurement.date >= '2016-08-18').all()
    session.close()

    tobs_results = []
    for date, tobs in tobs_hist:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        tobs_results.append(tobs_dict)
    return jsonify(tobs_results)


@app.route("/api/v1.0/<start>")
def temperature_by_start_date(start):
    session = Session(engine)
    
    tobs_results_by_start_date = session.query(Measurement.date, func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).group_by(Measurement.date).filter(Measurement.date >= start).all()
    session.close()

    temperature_results = []
    for date, min, max, avg in tobs_results_by_start_date:
        temperature_dict = {}
        temperature_dict['date'] = date
        temperature_dict['min'] = min
        temperature_dict['max'] = max
        temperature_dict['avg'] = avg
        temperature_results.append(temperature_dict)
    return jsonify(temperature_results)

@app.route("/api/v1.0/<start>/<end>")
def temperature_by_start_and_end_date(start, end):
    session = Session(engine)
    
    tobs_results_by_start_and_end_date = session.query(Measurement.date, func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).group_by(Measurement.date).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    temperature_results = []
    for date, min, max, avg in tobs_results_by_start_and_end_date:
        temperature_dict = {}
        temperature_dict['date'] = date
        temperature_dict['min'] = min
        temperature_dict['max'] = max
        temperature_dict['avg'] = avg
        temperature_results.append(temperature_dict)
    return jsonify(temperature_results)

if __name__ == '__main__':
    app.run(debug=True)
