
# This file provides get functions to get data from sensors.
# Two classes are avaliable, Sensor reads data from excel file 
# in order to test this package. 
# SensorSocket recieves data from sensors from an external server
# instead of reading an excel file.

import pandas as pd
from . import simulator as sim
from . import global_tools as tools
import os
import logging
import socket
import json
import time as t

# SETUP ERROR LOGGING AND DEBUGGING
logger = logging.getLogger(__name__)


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
        logger.debug("Path to excel data: "+ self.DATA_PATH)
        logger.debug("Sheet name: " + self.SHEET_NAME)
        logger.debug("Columns name in excel data: " + str(self.COLUMNS_NAME))

    def __get_excel_data(self):
        self.__excel_data = pd.read_excel(self.DATA_PATH, sheet_name=self.SHEET_NAME)
        self.__loaded_data = True
        #logger.debug(self.__excel_data)

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
        #logger.debug("Datos a extraer: ")
        #logger.debug(self.__excel_data[self.COLUMNS_NAME[0]][flightNumber*sim.TIME_BETWEEN_SIMULATIONS*60])
        #df = pd.DataFrame(self.__excel_data, columns=[self.COLUMNS_NAME[0]])
        #logger.debug("Numero de registro a consultar:" + str(flightNumber*sim.TIME_BETWEEN_SIMULATIONS*60))
        return self.__excel_data[self.COLUMNS_NAME[0]][flightNumber*sim.TIME_BETWEEN_SIMULATIONS*60]

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
        #logger.debug("Datos a extraer: ")
        #logger.debug(self.__excel_data[self.COLUMNS_NAME[1]][flightNumber * sim.TIME_BETWEEN_SIMULATIONS * 60])
        # df = pd.DataFrame(self.__excel_data, columns=[self.COLUMNS_NAME[1]])
        #logger.debug("Numero de registro a consultar:" + str(flightNumber * sim.TIME_BETWEEN_SIMULATIONS * 60))
        return self.__excel_data[self.COLUMNS_NAME[1]][flightNumber * sim.TIME_BETWEEN_SIMULATIONS * 60]

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
        #logger.debug("Datos a extraer: ")
        #logger.debug(self.__excel_data[self.COLUMNS_NAME[2]][flightNumber * sim.TIME_BETWEEN_SIMULATIONS * 60])
        # df = pd.DataFrame(self.__excel_data, columns=[self.COLUMNS_NAME[2]])
        #logger.debug("Numero de registro a consultar:" + str(flightNumber * sim.TIME_BETWEEN_SIMULATIONS * 60))
        return self.__excel_data[self.COLUMNS_NAME[2]][flightNumber * sim.TIME_BETWEEN_SIMULATIONS * 60]

    def has_burst(self, flightNumber):
        #return eval(input('Indique si el globo ya ha explotado'))
        return flightNumber * sim.TIME_BETWEEN_SIMULATIONS * 60 > 3290

    def getWinduvSpeed(self, lat, lon, alt, time, flightNumber):
        if not self.__loaded_data:
            self.__get_excel_data()
        #dlat = -2*10**(-6) #grados/seg
        #dlong = -6*10**(-6) #grados/seg
        #return tools.deg2m(dlat, dlong, 39.573174) #ya en m/s
        #vel hor:
        long1 = self.__excel_data[self.COLUMNS_NAME[1]][flightNumber * sim.TIME_BETWEEN_SIMULATIONS * 60]
        long2 = self.__excel_data[self.COLUMNS_NAME[1]][flightNumber * sim.TIME_BETWEEN_SIMULATIONS * 60+1]
        #logger.debug("long1: {}-long2: {}".format(long1, long2))
        u = tools.haversine(0, long1, 0, long2)
        #vel ver:
        lat1 = self.__excel_data[self.COLUMNS_NAME[0]][flightNumber * sim.TIME_BETWEEN_SIMULATIONS * 60]
        lat2 = self.__excel_data[self.COLUMNS_NAME[0]][flightNumber * sim.TIME_BETWEEN_SIMULATIONS * 60+1]
        #logger.debug("lat1: {}-lat2: {}".format(lat1, lat2))
        v = tools.haversine(lat1, 0, lat2, 0)
        return u, v

    def getVerticalSpeed(self, flightNumber):
        data = pd.read_excel(self.DATA_PATH, sheet_name="Vel.Vertical V4")
        logger.debug("Reading vertical speed sheet, elev:" +
                     str(data['Vel. (m/s)'][flightNumber * sim.TIME_BETWEEN_SIMULATIONS * 60]))
        return data['Vel. (m/s)'][flightNumber * sim.TIME_BETWEEN_SIMULATIONS * 60]

    #TODO: the following functions may not be needed

    def getTemperature(self, flightNumber):
        """
        Gets temperature in degrees celsius from sensors

        Parameters
        ----------
            None

        Returns
        -------
            result : float (degrees celsius)
        """
        if not self.__loaded_data:
            self.__get_excel_data()
        return self.__excel_data[self.COLUMNS_NAME[3]][flightNumber * sim.TIME_BETWEEN_SIMULATIONS * 60]

    def getWindDirection(self):
        """
        Gets wind direction in degrees clockwise from north from sensors

        Parameters
        ----------
            None

        Returns
        -------
            result : float (degrees from north)
        """
        if not self.__loaded_data:
            self.__get_excel_data()
        return pd.DataFrame(self.__excel_data, columns=self.COLUMNS_NAME[4])

    def getPressure(self):
        """
        Gets Pressure in milibar from sensors

        Parameters
        ----------
            None

        Returns
        -------
            result : float (milibar)
        """
        if not self.__loaded_data:
            self.__get_excel_data()
        return pd.DataFrame(self.__excel_data, columns=self.COLUMNS_NAME[7])

class SensorSocket(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        #this var is needed for testing
        self.other_sensor = Sensor()

        # self.dic = {
        #             "temp": 12,
        #             "press": 13,
        #             "lat": 5,
        #             "lon": 6,
        #             "alt": 7,
        #             "vel_vert": -2,
        #             "burst": 0, 
        # }
        self.dic = {
                    "temp": 4,
                    "press": 5,
                    "lat": 1,
                    "lon": 2,
                    "alt": 3,
                    "vel_vert": 6,
                    "burst": 0,
        }
    
    def get_param(self, msg):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            #logger.debug('conectado')
            #print(s)
            s.sendall(str(msg).encode('utf-8'))
            #print('enviado')
            data = s.recv(1024)
            data = repr(data).strip("b'")
            #logger.debug("RECIEVED----:"+data)
        return data.split(',')

    def getAltitude(self):
        return float(self.get_param('hola')[self.dic['alt']])

    def getLon(self,a=0):
        return float(self.get_param('hola')[self.dic['lon']])

    def getLat(self, a=0):
        b = self.get_param('hola')[self.dic['lat']]
        #logger.debug("traza en sensor tools lat-------"+b)
        return float(b)

    def has_burst(self):
        return json.loads(self.get_param('hola')[self.dic['burst']].lower())

    def getTemperature(self):
        return  float(self.get_param('hola')[self.dic['temp']])
    
    def getPressure(self):
        return  float(self.get_param('hola')[self.dic['press']])

    def getVerticalSpeed(self):
        return  float(self.get_param('hola')[self.dic['vel_vert']])

    def getWinduvSpeed(self, lat, lon, alt, time, flightNumber=10):
        # TIME_SLEEP = 0.1 #time between each question in asking lat and long in seconds
        # #vel hor:
        # long1 = self.getLon('hola')
        # lat1 = self.getLat('hola')
        
        # t.sleep(TIME_SLEEP)
        # lat2 = self.getLat(a=1)
        # long2 = self.getLon(a=1)
        # #logger.debug("long1: {}-long2: {}".format(long1, long2))
        # u = tools.haversine(0, long1, 0, long2)/TIME_SLEEP
               
        # #logger.debug("lat1: {}-lat2: {}".format(lat1, lat2))
        # v = tools.haversine(lat1, 0, lat2, 0)/TIME_SLEEP
        return self.other_sensor.getWinduvSpeed(lat, lon, alt, time, flightNumber)
        #return u, v

    def send_prediction(self, lat, long):
        msg = str(lat)+","+str(long)
        logger.debug("SENDING PREDICTION: "+ msg)
        self.get_param(msg)
