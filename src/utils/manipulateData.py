import geopandas as gpd
import pandas as pd
from pyproj import CRS
# imports below are for the kde function, might need refactoring
import numpy as np
import seaborn as sns

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
    # refactor: maybe have a function that adds "accumulated_" tag automatically to list
    accumulation_df = initializeAccumulationDataFrame(gdf,
                                                      columns_of_interest)  # reprojection must have already been done!
    accumulation_gdf = geoDataFrameFromDataFrame(accumulation_df, crs)
    # NB : currently i am destroying and recreating latitudes x and y everytime,
    # perhaps can refactor by keeping longitude and latitude oclumns that i then parse to seaborn kdeplot
    new_columns = ['geometry']
    accumulated_columns = [f"accumulated_{column}" for column in columns_of_interest]
    new_columns.extend(accumulated_columns)
    # accumulation_gdf.drop([LONGITUDE_COLUMN, LATITUDE_COLUMN])  its ok bc of geometry column
    accumulation_gdf = accumulation_gdf[new_columns]
    return accumulation_gdf


def obtainGeoDataFromTimeStep(gdf: gpd.GeoDataFrame, timestep: int, columns_of_interest: list):
    columns = [LONGITUDE_COLUMN, LATITUDE_COLUMN]
    columns.extend(columns_of_interest)
    timestep_gdf = gdf.loc[
        gdf[TIMESTEP_COLUMN] == timestep, columns]
    return timestep_gdf


"""def indexDataFrameWithLonLat(df: pd.DataFrame):
    df.reset_index(inplace=True)
    df.set_index([LONGITUDE_COLUMN, LATITUDE_COLUMN], inplace=True)


def indexGeoDataFrameWithGeometry(gdf: gpd.GeoDataFrame):
    geometry = gdf.geometry
    gdf.reset_index(inplace=True)
    gdf.set_index(GEOMETRY_COLUMN, inplace=True)
    gdf.set_geometry
    # oh god probably all of my code is catastrophic and i just
    # still do not append accumulation data properly and also mess up the geometry
    """


def addAccumulationDataFromGeoDataFrame(accumulation_gdf: gpd.GeoDataFrame,
                                        timestep_gdf: gpd.GeoDataFrame,
                                        columns_of_interest: list):
    # assumes sorted
    # NB : in refactoring, make it so it's clear what the columns of interest are : gases set in project variables
    # and never touched again.
    # NB : this function is funky and crucial and should be tested.

    # this attempt : merges and unmerges
    merged_gdf = accumulation_gdf.merge(timestep_gdf, on='geometry', how='left')
    for column in columns_of_interest:
        merged_gdf[f'accumulated_{column}'] += merged_gdf[column].fillna(0)
    # print(merged_gdf)
    accumulation_gdf = merged_gdf[accumulation_gdf.columns]
    # print(accumulation_gdf)
    return accumulation_gdf


def getEndValuesFromGeoDataFrame(gdf: gpd.GeoDataFrame, column: str):
    geographical_sum = gdf.groupby([LONGITUDE_COLUMN, LATITUDE_COLUMN])[column].sum()
    return geographical_sum


def getPointMaximumFromGeoDataFrame(gdf: gpd.GeoDataFrame, column: str):
    geographical_sum = getEndValuesFromGeoDataFrame(gdf, column)
    return geographical_sum.max()


# might need some refactoring, there's starting to be a lot of functions...
def getKDEMaximumFromGeoDataFrame(gdf: gpd.GeoDataFrame, column: str):
    end_gdf = getEndValuesFromGeoDataFrame(gdf, column)
    kde = sns.kdeplot(x=end_gdf.geometry.x,  # ah ptn le nom de la colonne
                      y=end_gdf.geometry.y,
                      weights=end_gdf[column],
                      common_norm=False,
                      bw_method="silverman"
                      # vmin=0,  # doesn't seem to work, create a colorbar seperately?
                      # vmax=column_max
                      # cbar_kws={'shrink': COLORBAR_SHRINK}
                      )
    density_estimates = kde.get_array()
    max_density = np.max(density_estimates)
    return max_density


def getSimulatedTimeFromGeoDataFrame(gdf: gpd.GeoDataFrame):
    min_timestep = gdf[TIMESTEP_COLUMN].min()
    max_timestep = gdf[TIMESTEP_COLUMN].max()
    return max_timestep - min_timestep
