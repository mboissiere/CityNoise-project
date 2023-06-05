import geopandas as gpd
import pandas as pd
from pyproj import CRS

from src.utils.constants.manipulateDataConstants import *


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

    df = pd.read_csv(TRAFFIC_DATA_PATH,
                     usecols=[TIMESTEP_COLUMN,
                              LONGITUDE_COLUMN,
                              LATITUDE_COLUMN].append(columns),
                     dtype={TIMESTEP_COLUMN: TIMESTEP_TYPE,
                            LONGITUDE_COLUMN: LONGITUDE_TYPE,
                            LATITUDE_COLUMN: LATITUDE_TYPE}).dropna()
    return df


def initializeAccumulationDataFrame(df: pd.DataFrame, columns_of_interest: list):
    df.sort_values(TIMESTEP_COLUMN)
    accumulation_df = df.drop_duplicates([LONGITUDE_COLUMN, LATITUDE_COLUMN])
    accumulation_columns = list()
    for column in columns_of_interest:
        accumulation_df[f'accumulated_{column}'] = 0
        accumulation_columns.append(f'accumulated_{column}')
    accumulation_df = accumulation_df[[LONGITUDE_COLUMN, LATITUDE_COLUMN].extend(accumulation_columns)]
    accumulation_df = accumulation_df.sort_values([LONGITUDE_COLUMN, LATITUDE_COLUMN])
    accumulation_df = accumulation_df.reset_index(drop=True)
    return accumulation_df


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


def obtainGeoDataFromTimeStep(gdf: gpd.GeoDataFrame, timestep: int, columns_of_interest: list):
    timestep_gdf = gdf.loc[
        gdf[TIMESTEP_COLUMN] == timestep, [LONGITUDE_COLUMN, LATITUDE_COLUMN].extend(columns_of_interest)]
    return timestep_gdf


def indexGeoDataFrameWithLonLat(gdf: gpd.GeoDataFrame):
    gdf.reset_index(inplace=True)
    gdf.set_index([LONGITUDE_COLUMN, LATITUDE_COLUMN], inplace=True)


def addAccumulationDataFromGeoDataFrame(accumulation_gdf: gpd.GeoDataFrame,
                                        timestep_gdf: gpd.GeoDataFrame,
                                        columns_of_interest: list):
    # assumes sorted
    # NB : in refactoring, make it so it's clear what the columns of interest are : gases set in project variables
    # and never touched again.
    # NB : this function is funky and crucial and should be tested.
    for column in columns_of_interest:
        accumulation_gdf.loc[timestep_gdf.index, f'accumulated_{column}'] += timestep_gdf[column].values


def simulatedTimeFromGeoDataFrame(gdf: gpd.GeoDataFrame):
    min_timestep = gdf[TIMESTEP_COLUMN].min()
    max_timestep = gdf[TIMESTEP_COLUMN].max()
    return max_timestep - min_timestep
