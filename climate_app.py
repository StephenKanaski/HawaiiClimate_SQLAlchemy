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

## Flask Routes ##

@app.route("/")




if __name__ == '__main__':
	app.run(debug=True)
