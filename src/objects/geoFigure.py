import geopandas
import matplotlib.pyplot as plt
import seaborn as sns

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
                           # edgecolor=SCATTER_EDGECOLOR,
                           linewidth=SCATTER_LINEWIDTH
                           )

    def createHeatMapFromGeoDataFrame(self, gdf: geopandas.GeoDataFrame, column: str):
        # TODO: very probably adapt for multiple columns if I don't do CO2eq
        colormap = sns.color_palette(COLORMAP, as_cmap=True)
        colormap.set_under(alpha=0.0)
        sns.heatmap(gdf[column],
                    cmap=colormap,
                    # cbar_kws={"shrink": 0.7, "vmin": 0, "vmax": 100}
                    alpha=HEATMAP_ALPHA,
                    vmin=0,  # np.nextafter(0, 1)
                    ax=self.ax)

    def addBasemapFromGeoDataFrame(self, gdf: geopandas.GeoDataFrame):
        # basemap_extent = gdf.total_bounds
        ctx.add_basemap(self.ax,
                        crs=gdf.crs,
                        # extent=basemap_extent,
                        source=BASEMAP_SOURCE,
                        alpha=BASEMAP_ALPHA,
                        zoom=BASEMAP_ZOOM)
