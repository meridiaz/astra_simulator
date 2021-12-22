# This file provides a simpler and less accurate program 
# to calcule balloon landing given data from sensors

# This program only calculates landing point when balloon
# is in de descent phase

# assumptions:
# - same wind in same altitude at different coordinates
# - descent rate is ascent phase is constant and set to 5 m/s
# - descent rate is descent phase is constant and set to the one
# collected from sensors before each simulation


# errors are 3-10 km when balloon has just exploded
# but when the balloon is close to landing the errors
# decrease to 0.2-3 km

# next package is to collect data from server
# currently not used
from astra.sensor_tools import SensorSocket
import astra.global_tools as tools
import numpy as np
import time as t

import os
import pandas as pd

TIME_BETWEEN_REQUESTS = 10  # time to sleep in each request to server in seconds 
NUMBER_SIMULATIONS = 500
DESCENT_RATE = 5 # speed of descent phase in m/s
ERROR_ALTS = 100 # error tolerated in altitudes in m


# this class is to read excel file and test the behavior
# of this program
class Sensor(object):

    def __init__(self, data_path='astra/sensors_data/V4.xlsx',
                sheet_name='Todo menos inicio y final',
                 columns_name=['Latitud', 'Longuitud', 'Altura', 'T2', 'Yaw', 'VelX', 'VelY', 'pres']):
        self.DATA_PATH = os.path.abspath(data_path)
        self.SHEET_NAME = sheet_name
        #This variable must always have the values in the following order:
        # Latitude, longitude, altitude, temperature, wind direction,
        # wind speed, pressure
        self.COLUMNS_NAME = columns_name
        self.__loaded_data = False
        self.__excel_data = None
        self.__vert_speed = None
        self.__loaded_data_speed = False
        """ print("Path to excel data: "+ self.DATA_PATH)
        print("Sheet name: " + self.SHEET_NAME)
        print("Columns name in excel data: " + str(self.COLUMNS_NAME)) """

    def __get_excel_data(self):
        self.__excel_data = pd.read_excel(self.DATA_PATH, sheet_name=self.SHEET_NAME)
        self.__loaded_data = True
        #print(self.__excel_data)

    def getLat(self, flightNumber):
        """
        Gets Latitude in degrees from sensors

        Parameters
        ----------
            flightNumber: int,  in order to take data from sensors every two minutes

        Returns
        -------
            result : float (degrees)
        """
        if not self.__loaded_data:
            self.__get_excel_data()
        #print("Datos a extraer: ")
        #print(self.__excel_data[self.COLUMNS_NAME[0]][flightNumber*TIME_BETWEEN_REQUESTS])
        #df = pd.DataFrame(self.__excel_data, columns=[self.COLUMNS_NAME[0]])
        #print("Numero de registro a consultar:" + str(flightNumber*TIME_BETWEEN_REQUESTS))
        return self.__excel_data[self.COLUMNS_NAME[0]][flightNumber*TIME_BETWEEN_REQUESTS]

    def getLon(self, flightNumber):
        """
        Gets longitude in degrees from sensors

        Parameters
        ----------
            flightNumber: int, in order to take data from sensors every two minutes

        Returns
        -------
            result : float (degrees)
        """
        if not self.__loaded_data:
            self.__get_excel_data()
        #print("Datos a extraer: ")
        #print(self.__excel_data[self.COLUMNS_NAME[1]][flightNumber * TIME_BETWEEN_REQUESTS])
        # df = pd.DataFrame(self.__excel_data, columns=[self.COLUMNS_NAME[1]])
        #print("Numero de registro a consultar:" + str(flightNumber * TIME_BETWEEN_REQUESTS))
        return self.__excel_data[self.COLUMNS_NAME[1]][flightNumber * TIME_BETWEEN_REQUESTS]

    def getAltitude(self, flightNumber):
        """
        Gets altitude of the balloon in meters from sensors

        Parameters
        ----------
            flightNumber: int, in order to take data from sensors every two minutes

        Returns
        -------
            result : float (meters)
        """
        if not self.__loaded_data:
            self.__get_excel_data()
        #print("Datos a extraer: ")
        #print(self.__excel_data[self.COLUMNS_NAME[2]][flightNumber * TIME_BETWEEN_REQUESTS])
        # df = pd.DataFrame(self.__excel_data, columns=[self.COLUMNS_NAME[2]])
        #print("Numero de registro a consultar:" + str(flightNumber * TIME_BETWEEN_REQUESTS))
        return self.__excel_data[self.COLUMNS_NAME[2]][flightNumber * TIME_BETWEEN_REQUESTS]
    def getVerticalSpeed(self, flightNumber):
        if not self.__loaded_data_speed:
            self.__vel_vert = pd.read_excel(self.DATA_PATH, sheet_name="Vel.Vertical V4")
            self.__loaded_data_speed = True
        return self.__vel_vert['Vel. (m/s)'][flightNumber * TIME_BETWEEN_REQUESTS]

    def has_burst(self, flightNumber):
        #return eval(input('Indique si el globo ya ha explotado'))
        if flightNumber * TIME_BETWEEN_REQUESTS > 3290:
            print('HAS BURSTED----')
        return flightNumber * TIME_BETWEEN_REQUESTS > 3290

def calculate_wind(new_lat, old_lat, new_lon, old_lon):
    sign_lat = np.sign(new_lat - old_lat)
    sign_lon = np.sign(new_lon - old_lon)
    modulus_lat = tools.haversine(old_lat, 0, new_lat, 0) /TIME_BETWEEN_REQUESTS
    modulus_lon = tools.haversine(0, old_lon, 0, new_lon) /TIME_BETWEEN_REQUESTS

    return sign_lat*modulus_lat, sign_lon*modulus_lon

def calculate_landing(u_wind, v_wind, alts, last_lat, last_lon, burst, ver_speed):
    lastDriftLat = 0.0
    lastDriftLon = 0.0
    landing_lat = 0.0
    landing_lon = 0.0

    # following vars stores all latitude and longitude landing
    # point
    lat_profile = []
    lon_profile = []
    alt_profile = []
    alt_profile.append(alts[-1])
    
    #Store the drift in meters (this is the distance between the
    for i in range(len(u_wind)):
        # calculate next alt
        # in testing fixed speed at 5m/s provided better results
        if has_burst:
            new_alt = alt_profile[i] + ver_speed*TIME_BETWEEN_REQUESTS
            #print("vel vert:"+str(ver_speed))
        else:
            new_alt = alt_profile[i] - DESCENT_RATE*TIME_BETWEEN_REQUESTS
       
        alt_profile.append(new_alt)
        # find closest alt
        index = tools.find_nearest_index(alts, new_alt)
        #print("real alt vs simulated", str(new_alt), str(alts[index]))
        
        # check error between altitudes
        if np.abs(new_alt-alts[index]) > ERROR_ALTS:
            print("Could not find a suitable altitude")
            break
        
        if alts[index] == alts[-1]:
            index = index - 1
        lastDriftLat += v_wind[index] * TIME_BETWEEN_REQUESTS
        lastDriftLon += u_wind[index] * TIME_BETWEEN_REQUESTS
        # Convert it to degrees
        dLat, dLon = tools.m2deg(lastDriftLat, lastDriftLon, landing_lat)
        # Store the new latitude and longitude
        landing_lat = last_lat + dLat
        landing_lon = last_lon + dLon


        # Check that latitude and longitude are within bounds and correct if
        # they are not (for example, if the balloon flew over the North or the
        # South Pole).
        if landing_lat > 90:
            landing_lat = 180 - landing_lat
            landing_lon += 180
        elif landing_lat < -90:
            landing_lat = -180 - landing_lat
            landing_lon += 180

        if landing_lon > 180:
            n = int(landing_lon-180)/360 + 1
            landing_lon -= n * 360
        elif landing_lon <= -180:
            n = int(abs(landing_lon)-180)/360 + 1
            landing_lon += n * 360

        lat_profile.append(landing_lat)
        lon_profile.append(landing_lon)


        
    if len(lat_profile) != 0:
        print(f"landing will be in: {lat_profile[-1]}, {lon_profile[-1]}." + \
            f" Estimated at: {alts[-1]}")
        # send prediction:
        #sen.send_prediction(landing_lat, landing_lon)

        return lat_profile[-1], lon_profile[-1], alt_profile[-1]
    return -1, -1, -1
        

#sensor = SensorSocket(HOST, PORT)
#TODO: this line is for testing:
sensor = Sensor()


flight_number = 0

lat_ascent = []
lon_ascent = []
altitudes = []

lat_prof = []
lon_prof = []
u_wind = []
v_wind = []

last_alt = 0

for flight_number in range(NUMBER_SIMULATIONS):
    # collect altitude and coordinates
    has_burst = sensor.has_burst(flight_number)
    lat_ascent.append(sensor.getLat(flight_number))
    lon_ascent.append(sensor.getLon(flight_number))
    altitudes.append(sensor.getAltitude(flight_number))
    ver_speed = sensor.getVerticalSpeed(flight_number)
    
    # calculate landing coordinate simulating the last altitude
    # collected is the altitude where the balloon bursts
    if len(altitudes) > 1:
        # calcute wind in each altitude given coordinates collected before
        v_wind_it, u_wind_it = calculate_wind(lat_ascent[-1], lat_ascent[-2],
                                              lon_ascent[-1], lon_ascent[-2])
        u_wind.append(u_wind_it)
        v_wind.append(v_wind_it)
        lat_land, lon_land, last_alt = calculate_landing(u_wind, v_wind, altitudes, 
                                                lat_ascent[-1], lon_ascent[-1], has_burst, ver_speed)
        # store landing results:
        lat_prof.append(lat_land)
        lon_prof.append(lon_prof)

        #TODO: uncomment for real launching
        # t.sleep(TIME_BETWEEN_REQUESTS)
        flight_number = flight_number + 1


#print(altitudes)


