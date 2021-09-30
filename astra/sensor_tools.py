#create getLat(), getLon(), getPressure, hasBurst()
#getElev(), getWindDirection(), getWindSpeed(), getTemperature()?

import pandas as pd
from . import simulator as sim
from . import global_tools as tools
import os

# This file provides get functions to get data from sensors.
# In case of testing this method obtain data from excel file

class Sensor(object):

    def __init__(self, data_path='astra_simulator/astra/sensors_data/V4.xlsx',
                sheet_name='V4 Volcado SD RAW 9',
                 columns_name=['Latitud', 'Longitud', 'Altura', 'TempOut', 'Yaw', 'VelX', 'VelY', 'Presion']):
        self.DATA_PATH = os.path.abspath(data_path)
        self.SHEET_NAME = sheet_name
        #This variable must always have the values in the following order:
        # Latitude, longitude, altitude, temperature, wind direction,
        # wind speed, pressure
        self.COLUMNS_NAME = columns_name
        self.__excel_data = None

    def __get_excel_data(self):
        self.__excel_data = pd.read_excel (self.DATA_PATH, sheet_name=self.SHEET_NAME)
        print(self.__excel_data)

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
        if self.__excel_data == None:
            self.__excel_data = self.__get_excel_data()
        df = pd.DataFrame(self.__excel_data, columns=self.COLUMNS_NAME[0])
        print("numero de registro a consultar:" + (flightNumber*sim.TIME_BETWEEN_SIMULATIONS*60+2))
        return df[flightNumber*sim.TIME_BETWEEN_SIMULATIONS*60]

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
        if self.__excel_data == None:
            self.__excel_data = self.__get_excel_data()
        df = pd.DataFrame(self.__excel_data, columns=self.COLUMNS_NAME[1])
        print("numero de registro a consultar:" + (flightNumber*sim.TIME_BETWEEN_SIMULATIONS*60+2))
        return df[flightNumber*sim.TIME_BETWEEN_SIMULATIONS*60]

    def getElev(self, flightNumber):
        """
        Gets elevation in meters from sensors

        Parameters
        ----------
            flightNumber: int, in order to take data from sensors every two minutes

        Returns
        -------
            result : float (meters)
        """
        if self.__excel_data == None:
            self.__excel_data = self.__get_excel_data()
        df = pd.DataFrame(self.__excel_data, columns=self.COLUMNS_NAME[2])
        print("numero de registro a consultar:" + (flightNumber*sim.TIME_BETWEEN_SIMULATIONS*60+2))
        return df[flightNumber*sim.TIME_BETWEEN_SIMULATIONS*60]

    def has_burst(self):
        return eval(input('Indique si el globo ya ha explotado'))

    def getWinduvSpeed(self):
        dlat = -2*10**(-6) #grados/seg
        dlong = -6*10**(-6) #grados/seg
        return tools.deg2m(dlat, dlong, 39.573174) #ya en m/s


    #TODO: the following functions may not be needed

    def getTemperature(self):
        """
        Gets temperature in degrees celsius from sensors

        Parameters
        ----------
            None

        Returns
        -------
            result : float (degrees celsius)
        """
        if self.excel_data == None:
            self.__excel_data = self.__get_excel_data()
        return pd.DataFrame(self.__excel_data, columns=self.COLUMNS_NAME[3])

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
        if self.excel_data == None:
            self.__excel_data = self.__get_excel_data()
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
        if self.excel_data == None:
            self.__excel_data = self.__get_excel_data()
        return pd.DataFrame(self.__excel_data, columns=self.COLUMNS_NAME[0])


