import geopandas
import matplotlib.pyplot as plt

from src.objects.constants.geoFigureConstants import *


class GeoFigure(plt.Figure):
    def __init__(self, *args, **kwargs):
        if 'figsize' not in kwargs:
            kwargs['figsize'] = (FIGURE_SIZE_X, FIGURE_SIZE_Y)
        super().__init__(*args, **kwargs)

    def addGeoAxes(self, gdf: geopandas.GeoDataFrame):
        ax = self.add_subplot(SUBPLOT_NUMBER_ROWS, SUBPLOT_NUMBER_COLUMNS, SUBPLOT_INDEX)
        ax.set_aspect(AXES_ASPECT_MODE)
        if not SHOW_AXES:
            ax.set_axis_off()

        min_lon, min_lat, max_lon, max_lat = gdf.total_bounds
        ax.set_xlim(min_lon, max_lon)
        ax.set_ylim(min_lat, max_lat)
        return ax
