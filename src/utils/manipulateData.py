import geopandas as gpd
# imports below are for the kde function, might need refactoring
import numpy as np
import pandas as pd
from pyproj import CRS

from src.objects.constants.geoFigureConstants import *
from src.utils.constants.manipulateDataConstants import *

# TODO: Implement an import from .shp file if needed, it's part of Sacha's code.
'''.shp files are particularly interesting, since Geopandas GDFs (geometry column and all) can be exported into shp
(or geojson) files that can be opened in QGIS!'''

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
                              LATITUDE_COLUMN,
                              SPEED_COLUMN,
                              ACCELERATION_COLUMN,
                              GRADE_COLUMN].append(columns),
                     dtype={TIMESTEP_COLUMN: TIMESTEP_TYPE,
                            LONGITUDE_COLUMN: LONGITUDE_TYPE,
                            LATITUDE_COLUMN: LATITUDE_TYPE,
                            SPEED_COLUMN: SPEED_TYPE,
                            ACCELERATION_COLUMN: ACCELERATION_TYPE,
                            GRADE_COLUMN: GRADE_TYPE}).dropna()
    return df



def initializeAccumulationDataFrame(df: pd.DataFrame, columns_of_interest: list):
    df.sort_values(TIMESTEP_COLUMN)
    accumulation_df = df.drop_duplicates([LONGITUDE_COLUMN, LATITUDE_COLUMN])
    accumulation_columns = list()
    for column in columns_of_interest:
        accumulation_df[f'accumulated_{column}'] = 0
        accumulation_columns.append(f'accumulated_{column}')
    column_list = [LONGITUDE_COLUMN, LATITUDE_COLUMN]
    column_list.extend(accumulation_columns)
    accumulation_df = accumulation_df[column_list]
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


def initializeAccumulationGeoDataFrame(gdf: gpd.GeoDataFrame, columns_of_interest: list, crs: CRS):
    '''
    This function initialized, from a GeoDataFrame showcasing an evolution of values over time, a new "accumulation"
    GeoDataFrame that will compute the sum of values up to any certain timestep, efficiently.
    IMPORTANT: CRS reprojection must have already been done!

    :param gdf:
    :param columns_of_interest:
    :param crs:
    :return:
    '''
    # todo: maybe a function could automate adding an "accumulated_" tag automatically to any dataframe of interest
    accumulation_df = initializeAccumulationDataFrame(gdf,
                                                      columns_of_interest)
    accumulation_gdf = geoDataFrameFromDataFrame(accumulation_df, crs)
    new_columns = ['geometry']
    accumulated_columns = [f"accumulated_{column}" for column in columns_of_interest]
    new_columns.extend(accumulated_columns)
    accumulation_gdf = accumulation_gdf[new_columns]
    return accumulation_gdf


def obtainGeoDataFromTimeStep(gdf: gpd.GeoDataFrame, timestep: int, columns_of_interest: list):
    columns = [LONGITUDE_COLUMN, LATITUDE_COLUMN]
    columns.extend(columns_of_interest)
    timestep_gdf = gdf.loc[
        gdf[TIMESTEP_COLUMN] == timestep, columns]
    return timestep_gdf

def addAccumulationDataFromGeoDataFrame(accumulation_gdf: gpd.GeoDataFrame,
                                        timestep_gdf: gpd.GeoDataFrame,
                                        columns_of_interest: list):
    '''
    Given a GeoDataFrame meant for accumulating values at each point, on a loop over timesteps,
    this is the action inside the loop: adds values from timestep_gdf into our accumulation_gdf.
    NB: This function assumes that
    NOTE: This function is crucial and should be tested properly.

    :param accumulation_gdf: the 2D GeoDataFrame accumulating values of a scalar (sum of timesteps thus far)
    :param timestep_gdf: the 2D GeoDataFrame of current scalar values (current timestep state)
    :param columns_of_interest: the gases we're studying (set in config/projectVariables)
    :return: accumulation_gdf, updated to the current timestep
    :rtype gpd.GeoDataFrame:
    '''
    merged_gdf = accumulation_gdf.merge(timestep_gdf, on='geometry', how='left')
    for column in columns_of_interest:
        merged_gdf[f'accumulated_{column}'] += merged_gdf[column].fillna(0)
    accumulation_gdf = merged_gdf[accumulation_gdf.columns]
    return accumulation_gdf


def getEndValuesFromGeoDataFrame(gdf: gpd.GeoDataFrame, column: str):
    geographical_sum = gdf.groupby([LONGITUDE_COLUMN, LATITUDE_COLUMN])[column].sum().to_frame().reset_index()
    return geographical_sum


def getPointMaximumFromGeoDataFrame(gdf: gpd.GeoDataFrame, column: str):
    geographical_sum = getEndValuesFromGeoDataFrame(gdf, column)
    return geographical_sum.max()

# these should be its own function
def getHistogramMaximumFromGeoDataFrame(gdf: gpd.GeoDataFrame, column: str):
    end_gdf = getEndValuesFromGeoDataFrame(gdf, column)
    hist, _, _ = np.histogram2d(x=end_gdf[LONGITUDE_COLUMN],
                                y=end_gdf[LATITUDE_COLUMN],
                                weights=end_gdf[column],
                                bins=[HISTOGRAM_XBINS, HISTOGRAM_YBINS]
                                )
    max_density = np.max(hist)
    return max_density


def getSimulatedTimeFromGeoDataFrame(gdf: gpd.GeoDataFrame):
    min_timestep = gdf[TIMESTEP_COLUMN].min()
    max_timestep = gdf[TIMESTEP_COLUMN].max()
    return max_timestep - min_timestep
