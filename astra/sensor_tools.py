
# This file provides get functions to get data from sensors.
# In case of testing this method obtain data from excel file

import pandas as pd
from . import simulator as sim
from . import global_tools as tools
import os
import logging

# SETUP ERROR LOGGING AND DEBUGGING
logger = logging.getLogger(__name__)


class Sensor(object):

    def __init__(self, data_path='astra_simulator/astra/sensors_data/V4.xlsx',
                sheet_name='Todo menos inicio y final',
                 columns_name=['Latitud', 'Longuitud', 'Altura', 'TempOut', 'Yaw', 'VelX', 'VelY', 'Presion']):
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
        logger.debug(self.__excel_data)

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
        logger.debug("Datos a extraer: ")
        logger.debug(self.__excel_data[self.COLUMNS_NAME[0]][flightNumber*sim.TIME_BETWEEN_SIMULATIONS*60])
        #df = pd.DataFrame(self.__excel_data, columns=[self.COLUMNS_NAME[0]])
        logger.debug("Numero de registro a consultar:" + str(flightNumber*sim.TIME_BETWEEN_SIMULATIONS*60))
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
            self.__excel_data = self.__get_excel_data()
        logger.debug("Datos a extraer: ")
        logger.debug(self.__excel_data[self.COLUMNS_NAME[1]][flightNumber * sim.TIME_BETWEEN_SIMULATIONS * 60])
        # df = pd.DataFrame(self.__excel_data, columns=[self.COLUMNS_NAME[1]])
        logger.debug("Numero de registro a consultar:" + str(flightNumber * sim.TIME_BETWEEN_SIMULATIONS * 60))
        return self.__excel_data[self.COLUMNS_NAME[1]][flightNumber * sim.TIME_BETWEEN_SIMULATIONS * 60]

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
        if not self.__loaded_data:
            self.__excel_data = self.__get_excel_data()
        logger.debug("Datos a extraer: ")
        logger.debug(self.__excel_data[self.COLUMNS_NAME[2]][flightNumber * sim.TIME_BETWEEN_SIMULATIONS * 60])
        # df = pd.DataFrame(self.__excel_data, columns=[self.COLUMNS_NAME[2]])
        logger.debug("Numero de registro a consultar:" + str(flightNumber * sim.TIME_BETWEEN_SIMULATIONS * 60))
        return self.__excel_data[self.COLUMNS_NAME[2]][flightNumber * sim.TIME_BETWEEN_SIMULATIONS * 60]

    def has_burst(self, flightNumber):
        # TODO: this method should not recieve flight number
        #return eval(input('Indique si el globo ya ha explotado'))
        return flightNumber * sim.TIME_BETWEEN_SIMULATIONS * 60 > 3290

    def getWinduvSpeed():
        dlat = -2*10**(-6) #grados/seg
        dlong = -6*10**(-6) #grados/seg
        return tools.deg2m(dlat, dlong, 39.573174) #ya en m/s

    def getVerticalSpeed(self, flightNumber):
        # TODO: this method should not recieve flight number
        data = pd.read_excel(self.DATA_PATH, sheet_name="Vel.Vertical V4")
        logger.debug("Reading vertical speed sheet")
        return data['Vel. (m/s)'][flightNumber * sim.TIME_BETWEEN_SIMULATIONS * 60]

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
        if not self.__loaded_data:
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
        if not self.__loaded_data:
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
        if not self.__loaded_data:
            self.__excel_data = self.__get_excel_data()
        return pd.DataFrame(self.__excel_data, columns=self.COLUMNS_NAME[0])


