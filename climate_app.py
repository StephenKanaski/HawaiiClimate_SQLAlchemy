import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

## Database Setup ##

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

## Reflect Database and Reflect Tables##

Base = automap_base()
Base.prepare(engine, reflect=True)

## Save references to table(s)

Measurement = Base.classes.measurement
StationData = Base.classes.station

## Create Session ##

session = Session(engine)

## Setup/Initiate Flask ##

app = Flask(__name__)

## from bonus section:

# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

## Flask Routes ##

@app.route("/")
def welcome():
	"""List all available api routes."""
	return(
		f"Welcome to the Hawaii Climate Analysis Homepage!<br/>"
		f"Available Routes:<br/>"
		f"============================<br/>"
		f"Precipitation Data from 2016-08-23 to 2017-08-23<br/>"
		f"/api/v1.0/precipitation<br/>"
		f"============================<br/>"
		f"List Available Stations in Hawaii<br/>"
		f"/api/v1.0/stations<br/>"
		f"============================<br/>"
		f"Temperature Observations from 2016-08-23 to 2017-08-23<br/>"
		f"/api/v1.0/tobs<br/>"
		f"============================<br/>"
		f"Enter in start date (format: 2016-01-01) to see min, max, and avg temps from start date to end of observable data<br/>"
		f"/api/v1.0/<start><br/>"
		f"============================<br/>"
		f"Enter a date range (format: 2016-03-08/2016-05-10) to see min, max, and avg temps within that range<br/>"
		f"/api/v1.0/<start>/<end>")

'''final date in obervable data is 2017-08-23'''
begin_date = dt.date(2017, 8, 23) - dt.timedelta(365)

@app.route("/api/v1.0/precipitation")
def precipitation():
	print("Precipitation API Request Received.")

	'''Retrieve precipitation data from last 12 months and set to dictionary'''
	precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= begin_date).\
	order_by(Measurement.date).all()

	precip_obs = []
	for precip_data in precip:
		prcp_dict = {}
		prcp_dict["Date"] = precip_data.date
		prcp_dict["Precipitation"] = precip_data.prcp
		precip_obs.append(prcp_dict)


	'''jsonify dictionary'''
	return jsonify(precip_obs)

@app.route("/api/v1.0/stations")
def stations():
	print("Station API Request Received.")

	''' Columns in StationData: id, station, name, latitude, longitude, elevation '''
	''' query station table and set data to list of dictionaries '''
	stats = session.query(StationData).all()

	station_list = []
	for stat in stats:
		station_dict = {}
		station_dict["id"] = stat.id
		station_dict["station"] = stat.station
		station_dict["name"] = stat.name
		station_dict["latitude"] = stat.latitude
		station_dict["longitude"] = stat.longitude
		station_dict["elevation"] = stat.elevation
		station_list.append(station_dict)

	return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
	print("Observation API Request Received.")
	'''Measurement columns: id, station, date, prcp, tobs'''
	'''query date, station, and tobs from Measurement'''

	measures = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
	group_by(Measurement.date).filter(Measurement.date >= begin_date).\
	order_by(Measurement.station).all()

	tobs_list =[]
	for measure in measures:
		tobs_dict = {}
		tobs_dict["date"] = measure.date
		tobs_dict["station"] = measure.station
		tobs_dict["tobs"] = measure.tobs
		tobs_list.append(tobs_dict)

	return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start_range(start=None):
	'''Return json list of minimum, maximum, and average temperatures within a date range starting from date entered'''
	print("Start Date API Request Received")

	temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
	filter(Measurement.date >= start).all()

	temp_stats = []
	for Tmin, Tmax, Tavg in temps:
		temp_dict = {}
		temp_dict["Min Temperature"] = Tmin
		temp_dict["Max Temperature"] = Tmax
		temp_dict["Avg Temperature"] = Tavg
		temp_stats.append(temp_dict)

	return jsonify(temp_stats)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
	'''Return json of minimun, maximum, and average temperatures within a specified range'''
	print("Start and End Date API Request Received")

	temp_range = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
	filter(Measurement.date >= start).filter(Measurement.date <= end).all()

	range_stats = []

	for Tmin, Tmax, Tavg in temp_range:
		range_dict = {}
		range_dict["Min Temperature"] = Tmin
		range_dict["Max Temperature"] = Tmax
		range_dict["Avg Temperature"] = Tavg
		range_stats.append(range_dict)

	return jsonify(range_stats)


if __name__ == '__main__':
	app.run(debug=True)
