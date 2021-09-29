#create getLat(), getLon(), getPressure, hasBurst()
#getElev(), getWindDirection(), getWindSpeed(), getTemperature()?

import pandas as pd
from . import simulator as sim

# This file provides get functions to get data from sensors.
# In case of testing this method obtain data from excel file

DATA_PATH = './nombre.xlsx'
SHEET_NAME = 'nombre_hoja'
#This variable must always have the values in the following order:
# Latitude, longitude, altitude, temperature, wind direction, 
# wind speed, pressure
COLUMNS_NAME = ['Latitud', 'Longitud', 'Altitura', 'TempOut', 'Yaw', 'VelX', 'VelY', 'Presion']
__excel_data = None

def __get_excel_data():
    __excel_data = pd.read_excel (DATA_PATH, sheet_name=SHEET_NAME)
    print(__excel_data)

def getLat(flightNumber):
    """
    Gets Latitude in degrees from sensors

    Parameters
    ----------
        flightNumber: int,  in order to take data from sensors every two minutes

    Returns
    -------
        result : float (degrees)
    """
    if excel_data == None:
        __excel_data = __get_excel_data()
    df = pd.DataFrame(__excel_data, columns=COLUMNS_NAME[0])
    return df[flightNumber*sim.TIME_BETWEEN_SIMULATIONS*60]

def getLon(flightNumber):
    """
    Gets longitude in degrees from sensors

    Parameters
    ----------
        flightNumber: int, in order to take data from sensors every two minutes

    Returns
    -------
        result : float (degrees)
    """
    if excel_data == None:
        __excel_data = __get_excel_data()
    df = pd.DataFrame(__excel_data, columns=COLUMNS_NAME[1])
     return df[flightNumber*sim.TIME_BETWEEN_SIMULATIONS*60]

def getElev(flightNumber):
    """
    Gets elevation in meters from sensors

    Parameters
    ----------
        flightNumber: int, in order to take data from sensors every two minutes

    Returns
    -------
        result : float (meters)
    """
    if excel_data == None:
        __excel_data = __get_excel_data()
    df = pd.DataFrame(__excel_data, columns=COLUMNS_NAME[2])
    return df[flightNumber*sim.TIME_BETWEEN_SIMULATIONS*60]

#TODO: the following functions may not be needed

def getTemperature():
    """
    Gets temperature in degrees celsius from sensors

    Parameters
    ----------
        None

    Returns
    -------
        result : float (degrees celsius)
    """
    if excel_data == None:
        __excel_data = __get_excel_data()
    return pd.DataFrame(__excel_data, columns=COLUMNS_NAME[3])

def getWindDirection():
    """
    Gets wind direction in degrees clockwise from north from sensors

    Parameters
    ----------
        None

    Returns
    -------
        result : float (degrees from north)
    """
    if excel_data == None:
        __excel_data = __get_excel_data()
    return pd.DataFrame(__excel_data, columns=COLUMNS_NAME[4])

def getPressure():
    """
    Gets Pressure in milibar from sensors

    Parameters
    ----------
        None

    Returns
    -------
        result : float (milibar)
    """
    if excel_data == None:
        __excel_data = __get_excel_data()
    return pd.DataFrame(__excel_data, columns=COLUMNS_NAME[0])
    

