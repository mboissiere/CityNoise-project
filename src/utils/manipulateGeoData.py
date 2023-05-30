import pandas as pd
import geopandas as gpd
from pyproj import CRS
from src.constants.manipulateDataConstants import *


def geoDataFrameFromDataFrame(df, crs):
    geometry = gpd.points_from_xy(df[LONGITUDE_COLUMN], df[LATITUDE_COLUMN])
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs=crs)
    return gdf


def reprojectEPSG(gdf, input_EPSG, output_EPSG):
    input_CRS = CRS.from_epsg(input_EPSG)
    output_CRS = CRS.from_epsg(output_EPSG)
    gdf.to_crs(output_CRS)