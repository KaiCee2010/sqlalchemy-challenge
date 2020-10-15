# SQlAlchemy Challenge
## Repository Contents
This repository is for the sqlalchemy - challenge homework.  It contains:
* Climate.ipynb
* App.py
* Resources folder
    * contains source data
* Output folder
    * contains pngs of plots


## Climate.ipynb
Climate.ipynb contains code to:
* Climate Analysis and Exploration
* Precipitation Analysis
* Station Analysis
* Bonus Analysis
    * Temperature Analysis I
    * Temperature Analysis II
    * Daily Rainfall Average


## App.py
App.py contains code to:
* Create a climate app
* Use Flask to create your routes
* `/`
    * Home Page
* `/api/v1.0/precipitation`
    * Query results to a dictionary using `date` as the key and `prcp` as the value in JSON
* `/api/v1.0/stations`
    * Return a JSON list of stations from the dataset
* `/api/v1.0/stations_mostactives`
    * Return a JSON list of stations from the dataset with their record counts.
* `/api/v1.0/tobs`
    * Query the dates and temperature observations of the most active station for the last year of data and return a JSON list of temperature observations (TOBS) for the previous year
* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
    * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range
