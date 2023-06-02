import geopandas
import matplotlib.pyplot as plt

from src.objects.constants.geoFigureConstants import *


class GeoFigure:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(FIGURE_SIZE_X, FIGURE_SIZE_Y))
        self.ax.set_aspect(AXES_ASPECT_MODE)
        if not SHOW_AXES:
            self.ax.set_axis_off()

    def updateAxesFromGeoDataFrame(self, gdf: geopandas.GeoDataFrame):
        min_lon, min_lat, max_lon, max_lat = gdf.total_bounds
        self.ax.set_xlim(min_lon, max_lon)
        self.ax.set_ylim(min_lat, max_lat)

    def addScatterPlotFromGeoDataFrame(self, gdf: geopandas.GeoDataFrame):
        self.ax.scatter(gdf.geometry.x,
                        gdf.geometry.y,
                        color=SCATTER_COLOR,
                        s=SCATTER_SIZE,
                        marker=SCATTER_MARKER,
                        edgecolor=SCATTER_EDGECOLOR
                        )

    def updateScatterPlotFromGeoDataFrame(self, gdf: geopandas.GeoDataFrame):
        self.ax.scatter.set_offsets(list(zip(gdf.geometry.x, gdf.geometry.y)))

    def addBasemapFromGeoDataFrame(self, gdf: geopandas.GeoDataFrame):
        # basemap_extent = gdf.total_bounds
        ctx.add_basemap(self.ax,
                        crs=gdf.crs,
                        # extent=basemap_extent,
                        source=BASEMAP_SOURCE,
                        alpha=BASEMAP_ALPHA,
                        zoom=BASEMAP_ZOOM)
