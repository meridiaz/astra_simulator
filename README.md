# Landing predictor of HAB

This package gives accurate information about the landing area of a HAB (High Altitude Balloon). 
Before using it **check first_steps file**. Install all required packages by running the following command: `pip install -r requirements.txt`.

This package is based on the methodology and motion equations detailed in [Monte Carlo Paper](https://www.researchgate.net/publication/262990714_High-Altitude_Gas_Balloon_Trajectory_Prediction_A_Monte_Carlo_Model).

There are two files according to the approach taken. 
- simple_main.py file provides a solution which is less accurate but simpler and light code. Errors decrease as the balloon has already burst and its altitude is closer to the ground. On the other hand, landing points during ascent phase are not accurate. This program is intended for running it inside de payload of the balloon. 
- main.py which is more complex and is larger. But provides more accurate landing points in both phases, ascent and descent. It is possible to use this program to check, before the real launching, the landing area of the balloon. (also check requeriments in opentopodata/README.md file for installing opentopodata server)

## Main.py file
### How does it work?
- This package communicates with a server that gives the data collected from sensors in case of real launching. PORT and HOST are located in simulator.py file. Sensor_socket class from sensor_tools file creates a socket in each request which connects to the server located in PORT and HOST. The format of the response given by the server must be:

    `Has burst?, latitude, longitude, altitude, temperature, pressure, vertical speed`
    - Has burst is set to True if the balloon has burst, False if not.
    - Latitude and longitude must be in degrees.
    - Altitude in meters. 
    - Temperature in  degree Celsius. 
    - Pressure in milibars.
    - Vertical speed in meters/second. 
    - **Each variable must be separated by commas from the others.**

    It is also possible to use Sensor Class for testing. This class collects data from excel file.

- **Before using this package you must set launch date and time, in order to donwlod forecast wind, temperature and pressure.**

### How to use it?
**BOTH CASES NEED INTERNET CONNECTION IN ORDER TO DOWNLOAD WIND DATA, PRESSURE AND TEMPERATURE FROM GFS (Global Forecast System)**
    
- Predict landing point before launching de balloon: In this case original code astra_simulator will be executed. **ForecastEnvironment or SoundingEnvironment classes must be initialized**

    - It is possible to use a terrain elevation model by setting optional parameter elevation_model from Flight class in main.py file to True. Doing so, requests to a local server hosted in 5000 port will be made.

    It is important to note that if variable forecast_wind from Flight class in main.py file is set to False, will be ignored, for ForecastEnvironment it must be True.

- Predict landing point during balloon flight: In this case motion equations are the same as in previous event, but some improvements are implemented. **RealEnvironment class must be initialized**, if not some errors may be thrown. It is highly recommended to set optional parameter numberOfSimRuns from Flight class in main.py file to a high number such as 200, instead default value 10.

    - In this case is also possible to use a terrain elevation model in the same way as previous case.

    -  To test accuracy with an actual launch that occurred in the past, optional parameter forecast_wind from Flight class can be set to False in main.py file. Doing that, forecast wind won't be downloaded from GFS, instead u and v coordinates from wind will be calculated using drift from latitude and longitude stored in excel file. 
    In this case, wind is assumed to be constant for all altitudes in a single simulation. Therefore some simulations will be far away from the actual landing point.

    - Despite temperature and pressure can be taken from sensors, it is necessary to use a model that provides temperature and pressure at different altitudes and coordinates in a single simulation. This is done by downloading a forecast from GPS. In spite of that, model variables can be corrected by comparing them with actual temperatures and pressures collected from sensors, to do so, parameter correct_data from realEnvironment class must be set to True in main.py file.
    Note only temperature was avaliable when testing, so if pressure is also avaliable uncomment the code at the end of fly method in simulator.py file(a TODO mark indicates where it is located).

    - **IMPORTANT** Before real launching is necessary to uncomment sleep line after each simulation in run method, again a TODO mark indicates where it is located in simulator.py file. And it is recommended for real launching, to set forecast_wind, correct_data, elevation_model variables to True in main.py file.

    - Note that in main.py file maxFlightTime is set to 3 hours and cutdownAltitude to 35000m, if you  might think it is not enought for modeling your flight, feel free to increase it. If not unexpected behavior may occur.

## Simple_main.py file
### How does it work?
This program does not need Internet connection. 
This file collects coordinates and altitudes each TIME_BETWEEN_REQUESTS constant. Again uncomment sleep line after each simulation, a TODO mark indicates where it is located in simple_main.py. 

For each of the data collected it is assumed the new coordinate and altitude taken is where the balloon will burst, so at that moment calculates u and v wind vectors between last data collected and the previous values of the last data. Once the winds have been calculated it estimates the landing point assuming same winds between ascent and descent phase at each altitude but in different coordinates.
### Asumptions:
- Same winds at diferent coordinate but at same altitude
- For testing its behavior data is taken from excel file. 
- Descent rate during ascent phase it set to 5 m/s
- Descent rate during descent phase is set to the one collected from sensors at the beginning of each simulation.