from os.path import join
import os
import pandas as pd
from src.constants.manipulateDataConstants import *


# Construct the file path to the traffic data CSV file
traffic_data_path = os.path.join(PATH_TO_DATA, FILE_NAME_FROM_DATA)

# Read the CSV file into a Pandas dataframe
def importFromCSV(columns:list):
    """
    This function imports data from a CSV file into a Pandas DataFrame, assuming the CSV file has columns with timestep,
    longitude, and latitude.

    :param columns: A list of column names to be imported from the CSV.
    :return: A Pandas dataframe containing the desired columns, with rows containing #N/A entries removed.
    :rtype DataFrame:
    """
    df = pd.read_csv(traffic_data_path,
                    usecols=[TIMESTEP_COLUMN, LONGITUDE_COLUMN, LATITUDE_COLUMN].append(columns),
                    dtype={TIMESTEP_COLUMN: TIMESTEP_TYPE, LONGITUDE_COLUMN: LONGITUDE_TYPE, LATITUDE_COLUMN: LATITUDE_TYPE).dropna()
    return df
