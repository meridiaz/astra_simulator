This package gives accurate information about the landing area of a HAB (High Altitude Balloon)

Use cases:
    **BOTH CASES NEED INTERNET CONNECTION IN ORDER TO DOWNLOAD WIND DATA, PRESSURE AND TEMPERATURE FROM GFS (Global Forecast System)**
    
- Predict landing point before launching de balloon: In this case original code astra_simulator will be executed. **ForecastEnvironment or SoundingEnvironment classes must be initialized**

    - It is possible to use a terrain elevation model by setting optional parameter elevation_model from Flight class to True. Doing so, requests to a local server will be made.

    It is important to note that if variable forecast_wind from Flight class is set to False, will be ignore, for ForecastEnvironment it must be True.

- Predict landing point during balloon flight: In this case motion equations are the same as in previous event, but some improvements are implemented. **RealEnvironment class must be initialized**, if not some errors may be thrown. It is highly recommended to set optional parameter numberOfSimRuns from Flight class to a high number such as 200, instead default value 10.

    - In this case is also possible to use a terrain elevation model in the same way as previous case.

    -  To test accuracy with an actual launch that occurred in the past, optional parameter forecast_wind from Flight class can be set to False. Doing that, forecast wind won't be downloaded from GFS, instead u and v coordinates from wind will be calculated using drift from latitude and longitude stored in excel file. 
    In this case, wind is assumed to be constant for all altitudes in a single simulation. Therefore some simulations will be far away from the actual landing point.

    - Despite temperature and pressure can be taken from sensors, it is necessary to use a model that provides temperature and pressure at different altitudes in a simulation. This is done by downloading a forecast from GPS. In spite of that, model variables can be corrected by comparing them with actual temperatures and pressures collected from sensors, to do so, parameter correct_data from realEnvironment class must be set to True.
    Note only temperature was avaliable when testing, so if pressure is also avaliable uncomment the code at the end of fly method (a TODO mark indicates where it is located).

    - **IMPORTANT** Before real launching is necessary to uncomment sleep line after each simulation in run method, again a TODO mark indicates where it is located. 
    
    - It is recommeded for real launching, to set forecast_wind, correct_data, elevation_model variables to True.
