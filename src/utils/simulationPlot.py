"""
The aim of this module is to facilitate plotting in matplotlib and simplifying the functions for visualizing one, or
even several plots in the same figure.

That way, if I'm lost, confused, change my mind on modelling approach, it won't be a hassle!
Let's not that I'm not completely excluding the possibility of doing it over FEniCS, and include a gas dispersion
equation to solve. That being said, it seems very complicated for now, so let's start simple!
"""
import geopandas as gpd


def setAxesLimit(gdf: gpd.GeoDataFrame):
    min_lon, min_lat, max_lon, max_lat = gdf.total_bounds
