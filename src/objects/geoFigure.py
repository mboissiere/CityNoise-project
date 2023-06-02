import geopandas
import matplotlib.pyplot as plt

from src.objects.constants.geoFigureConstants import *


class GeoFigure:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(FIGURE_SIZE_X, FIGURE_SIZE_Y))

    def adjustAxesFromGeoDataFrame(self, gdf: geopandas.GeoDataFrame):
        self.ax.set_aspect(AXES_ASPECT_MODE)
        min_lon, min_lat, max_lon, max_lat = gdf.total_bounds
        self.ax.set_xlim(min_lon, max_lon)
        self.ax.set_ylim(min_lat, max_lat)
        if not SHOW_AXES:
            self.ax.set_axis_off()

    def createScatterPlotFromGeoDataFrame(self, gdf: geopandas.GeoDataFrame):
        self.ax = gdf.plot(color=SCATTER_COLOR,
                           marker=SCATTER_MARKER,
                           markersize=SCATTER_MARKERSIZE,
                           edgecolor=SCATTER_EDGECOLOR,
                           linewidth=SCATTER_LINEWIDTH
                           )

    def addBasemapFromGeoDataFrame(self, gdf: geopandas.GeoDataFrame):
        # basemap_extent = gdf.total_bounds
        ctx.add_basemap(self.ax,
                        crs=gdf.crs,
                        # extent=basemap_extent,
                        source=BASEMAP_SOURCE,
                        alpha=BASEMAP_ALPHA,
                        zoom=BASEMAP_ZOOM)
