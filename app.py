# 1. import Flask
from flask import Flask, jsonify
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect
#other dependencies
import numpy as np

#create connection to database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to my 'Home' page!<br/>"
        f"Here are all my Routes<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2012-02-28<br/>"
        f"/api/v1.0/2012-02-28/2013-02-28"
        )

# 4. Define what to do when a user hits the /precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'precipitation' page...")

    min_date = '2016-08-23'

    # Create our session (link) from Python to the DB
    session = Session(engine)
    prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > min_date).all() 
    session.close()

    return jsonify(prcp)


# 5. Define what to do when a user hits the /stations route
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'stations' page...")

    session = Session(engine)
    station_list = session.query(Measurement.station).group_by(Measurement.station).all()
    station_list = list(np.ravel(station_list))
    session.close()
    return jsonify(station_list)

#6. Define what to do when a user hits the /tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' page...")

    session = Session(engine)
    tobs_list = session.query(Measurement.tobs).all()
    tobs_list = list(np.ravel(tobs_list))
    session.close()
    return jsonify(tobs_list)
#-------------------------------------------------------------------------   
# 6. Define what to do when a user hits the <start> route



@app.route("/api/v1.0/<start>")
def temps_start(start):
    print("Server received request for '<start>' page...")
    session = Session(engine)
    x = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    return jsonify(x)
#-------------------------------------------------------------------------  
# 7. Define what to do when a user hits the <start><end> route

@app.route("/api/v1.0/<start>/<end>")
def temps_start_end(start, end):
    print("Server received request for <start>/<end> page...")

    session = Session(engine)
    y=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    return jsonify(y)


   

if __name__ == "__main__":
    app.run(debug=True)