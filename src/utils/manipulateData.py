import geopandas as gpd
import pandas as pd
from pyproj import CRS

from src.constants.manipulateDataConstants import *


# TODO: Implement an import from .shp file if needed, it's part of Sacha's code.


# Read the CSV file into a Pandas dataframe
def importFromCSV(columns: list):
    """
    This function imports data from a CSV file into a Pandas DataFrame, assuming the CSV file has columns with timestep,
    longitude, and latitude.

    So far the dtype argument doesn't impose a type on the columns.
    TODO: perhaps in a later version pollutants' columns could be modelled by a dictionary, just like the rest of dtype.

    :param columns: A list of column names to be imported from the CSV.
    :return: A Pandas dataframe containing the desired columns, with rows containing #N/A entries removed.
    :rtype DataFrame:
    """

    df = pd.read_csv(traffic_data_path,
                     usecols=[TIMESTEP_COLUMN,
                              LONGITUDE_COLUMN,
                              LATITUDE_COLUMN].append(columns),
                     dtype={TIMESTEP_COLUMN: TIMESTEP_TYPE,
                            LONGITUDE_COLUMN: LONGITUDE_TYPE,
                            LATITUDE_COLUMN: LATITUDE_TYPE}).dropna()
    return df


def geoDataFrameFromDataFrame(df: pd.DataFrame, crs: CRS):
    """
    This function converts a Pandas DataFrame object into a GeoPandas GeoDataFrame object,
    assuming the dataframe has longitude and latitude columns whose mapping follow a given CRS.

    Improvements of this method could perhaps include an exception to be raised if no longitude/latitude is found.

    :param df: The DataFrame object to be converted. Requires a longitude and latitude column.
    :param crs: The CRS of the mapping that the DataFrame object represents.
    :return: A GeoDataFrame object, now gaining additional methods by the GeoPandas module.
    :rtype GeoDataFrame:
    """
    geometry = gpd.points_from_xy(df[LONGITUDE_COLUMN], df[LATITUDE_COLUMN])
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs=crs)
    return gdf
