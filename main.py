# -*- coding: utf-8 -*-
# @Author: p-chambers
# @Date:   2017-05-18 17:55:28
# @Last Modified by:   p-chambers
# @Last Modified time: 2017-05-18 18:15:48
#if __name__ == "__main__":

from datetime import datetime, timedelta
import sys
import os
#sys.path.append(os.path.abspath('astra_simulator/astra'))
from astra.simulator import *
import astra.weather as weather
import logging
#from astra_simulator.astra import * 

# comment the code bellow if you want to check local server
# elevation requests 
logging.getLogger('requests').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

#pass 0 to UTCoffset in order to call global_tools.getUTCOffset
# la zona utc son 2h menos que en españa
# Environment parameters
# Launch site: Daytona Beach, FL
#        time: tomorrow, this time
launchSiteLat = 39.573517                 # deg
launchSiteLon = -3.5172               # deg
launchSiteElev = 704 #722                     # m
dateAndTime = datetime.now() + timedelta(days=1)
#dateAndTime = datetime(2021, 11, 11, 10, 15, 0)

simEnvironment = weather.RealEnvironment(launchSiteLat, launchSiteLon, launchSiteElev, dateAndTime, 
                                 debugging=True, inflationTemperature=0, 
                                UTC_offset=2.0, correct_data=True)
# simEnvironment = weather.ForecastEnvironment(launchSiteLat, launchSiteLon, launchSiteElev, dateAndTime, 
#                                  debugging=True, log_to_file=True, inflationTemperature=0, 
#                                  UTC_offset=2.0)

print(dateAndTime)

# Launch parameters
environment = simEnvironment
balloonGasType = 'Helium'
balloonModel = 'PACPR1600'
nozzleLift = 4.395#3.008#12.456#3.225#4.395                                # kg obtener de la calculadora del habhub
payloadTrainWeight = 2.8896                    # kg
parachuteModel = 'PX02'
numberOfSimRuns = 20
trainEquivSphereDiam = 0.1                    # m
cutdown = True
cutdownAltitude = 35000
excessPressureCoeff = 1
maxFlightTime = 10800 #2700seg = 7.5h #seconds

simFlight = Flight(balloonGasType, balloonModel, nozzleLift, payloadTrainWeight, environment,
                   parachuteModel=parachuteModel, numberOfSimRuns=numberOfSimRuns, 
                   trainEquivSphereDiam=trainEquivSphereDiam, cutdown=cutdown, cutdownAltitude=cutdownAltitude,
                   excessPressureCoeff=excessPressureCoeff, debugging=True, log_to_file=True, 
                   forecast_wind=False, elevation_model=True, maxFlightTime=maxFlightTime)

#simFlight.maxFlightTime = 5*60*60
simFlight.outputFile = os.path.join('../simulaciones', 'prueba_comp5')


# Run the simulation
simFlight.run()


