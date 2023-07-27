from math import sin, atan

from src.models.preprocessingConstants import *
from src.utils.manipulateData import *


# Messy architecture, shouldn't be importing from utils, but I'm working fast atm


# Formula for VSP from: https://doi.org/10.1016/j.trd.2017.05.016
# Formula for VSP mode pollutants: https://doi.org/10.1016/j.trd.2006.06.005

def computeVSP(speed, acceleration, slope):
    '''
    for a single value
    :param speed:
    :param acceleration:
    :param slope:
    :return:
    '''
    v = speed
    a = acceleration
    grade = slope

    vsp = v * (1.1 * a + 9.81 * sin(atan(grade)) + 0.132) + 0.000302 * v**3
    return vsp

def addVspToDataFrame(df: pd.DataFrame):
    '''operation on a dataframe'''
    df[VSP_COLUMN] = computeVSP(df[SPEED_COLUMN], df[ACCELERATION_COLUMN], df[GRADE_COLUMN])
    return df

def computeVspMode(vsp: float):
    if vsp < -2:
        return 1
    elif -2 <= vsp and vsp < 0:
        return 2
    elif 0 <= vsp and vsp < 1:
        return 3
    elif 1 <= vsp and vsp < 4:
        return 4
    elif 4 <= vsp and vsp < 7:
        return 5
    elif 7 <= vsp and vsp < 10:
        return 6
    elif 10 <= vsp and vsp < 13:
        return 7
    elif 13 <= vsp and vsp < 16:
        return 8
    elif 16 <= vsp and vsp < 19:
        return 9
    elif 19 <= vsp and vsp < 23:
        return 10
    elif 23 <= vsp and vsp < 28:
        return 11
    elif 28 <= vsp and vsp < 33:
        return 12
    elif 33 <= vsp and vsp < 39:
        return 13
    elif 39 <= vsp:
        return 14

def addVspModeToDataFrame(df: pd.DataFrame):
    df[MODE_COLUMN] = computeVspMode(df[VSP_COLUMN])
    return df

def importModelFromCSV(model: str):
    '''

    :param model: name of the csv with model, eg "Coelho2016" for Coelho2016.csv
    :return:
    '''


    df = pd.read_csv(f'{model}.csv',
                     #NB : Path here could be refactored
                     usecols=[MODE_COLUMN,
                              NOx_COLUMN,
                              HC_COLUMN,
                              CO2_COLUMN,
                              CO_COLUMN])
    return df

def addPollutantsToDataFrame(data_df: pd.DataFrame, model_df: pd.DataFrame):
    # Note: could be refactored with pollutant columns given in entry (projectVariables)
    data_df = data_df.merge(model_df[[MODE_COLUMN, CO2_COLUMN, NOx_COLUMN, HC_COLUMN, CO_COLUMN]], on=MODE_COLUMN, how='left')

    return data_df