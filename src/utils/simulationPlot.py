"""
The aim of this module is to facilitate plotting in matplotlib and simplifying the functions for visualizing one, or
even several plots in the same figure.

That way, if I'm lost, confused, change my mind on modelling approach, it won't be a hassle!
Let's not that I'm not completely excluding the possibility of doing it over FEniCS, and include a gas dispersion
equation to solve. That being said, it seems very complicated for now, so let's start simple!
"""
import geopandas as gpd
import matplotlib.pyplot as plt
from pyproj import CRS

from src.constants.simulationPlotConstants import *


def initializeFigureAndAxes(gdf: gpd.GeoDataFrame):
    """
    Initializes the area where the data will be plotted, using the bounds of the geographical data.

    :param gdf: The GeoDataFrame containing data of interest.*
    :return: The figure (Line2D object that will host the plot lines and markers)
    and the axes (Axes object that represents coordinates on which the plot is created)
    """
    fig, ax = plt.subplots(figsize=(FIGURE_SIZE_X, FIGURE_SIZE_Y))
    min_lon, min_lat, max_lon, max_lat = gdf.total_bounds
    ax.set_aspect(AXES_ASPECT_MODE)
    if not SHOW_AXES:
        ax.set_axis_off()
    ax.set_xlim(min_lon, max_lon)
    ax.set_ylim(min_lat, max_lat)
    return fig, ax


def addScatterPlotFromGeoDataFrame(gdf: gpd.GeoDataFrame):
    """
    Assuming one Axes object of interest, could change if for example there are different subplots

    :param gdf:
    :return:
    """
    gdf.plot(color=SCATTER_COLOR, size=SCATTER_SIZE, marker=SCATTER_MARKER)


def addBasemapFromCRS(crs: CRS):
    """
    Assuming one Axes object of interest, could change if for example there are different subplots

    :param gdf:
    :return:
    """
    ctx.add_basemap(crs=crs, source=BASEMAP_SOURCE, alpha=BASEMAP_ALPHA, zoom=BASEMAP_ZOOM)
