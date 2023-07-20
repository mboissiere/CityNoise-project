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
        self.ax.set_title("Air pollution simulation in Södermalm")
        # TODO: change plot title to auto-change if we're in another city (see location_name in projectVariables)
        self.ax.set_xlabel("Longitude")
        self.ax.set_ylabel("Latitude")

    def createScatterPlotFromGeoDataFrame(self, gdf: geopandas.GeoDataFrame):
        self.ax = gdf.plot(color=SCATTER_COLOR,
                           marker=SCATTER_MARKER,
                           markersize=SCATTER_MARKERSIZE,
                           edgecolor=SCATTER_EDGECOLOR,
                           linewidth=SCATTER_LINEWIDTH,
                           zorder=SCATTER_ZORDER
                           )


    def createHistogramPlotFromGeoDataFrame(self, gdf: geopandas.GeoDataFrame, column: str, column_max: float,
                                            max_unit: str):
        # todo: next step for modelling would be a mesh that actually makes sense (eg roundabouts, road segments, etc)
        # TODO: very probably adapt for multiple columns if I don't do CO2eq. but that might mean just, several plots.
        y = gdf.geometry.y
        weights = gdf[column]

        x_bins = HISTOGRAM_XBINS
        y_bins = HISTOGRAM_YBINS

        '''Possible alternative to setting it manually:
            x_min, x_max = x.min(), x.max()
            y_min, y_max = y.min(), y.max()
            length = x_max - x_min
            height = y_max - y_min
            length_over_height_ratio = length // height
            x_bins = int(length_over_height_ratio * HISTOGRAM_YBINS)
        
        OR linspace approach:
        
            x_bins = np.linspace(x_min, x_max, num=HISTOGRAM_XBINS)  # Adjust the number of bins as needed
            y_bins = np.linspace(y_min, y_max, num=HISTOGRAM_YBINS)
        
        So far, manual setting has been kept, it's simple and safe.
        '''

        self.ax = sns.histplot(x=x,
                               y=y,
                               weights=weights,
                               bins=[x_bins, y_bins],
                               cmap=COLORMAP, cbar=True,
                               cbar_kws={'label': f"CO2 Pollution ({max_unit})"  # ,
                                         # 'shrink': COLORBAR_SHRINK,
                                         },
                               vmin=0, vmax=column_max,
                               zorder=HISTOGRAM_ZORDER, alpha=HISTOGRAM_ALPHA)

    def addBasemapFromGeoDataFrame(self, gdf: geopandas.GeoDataFrame):
        # basemap_extent = gdf.total_bounds
        ctx.add_basemap(self.ax,
                        crs=gdf.crs,
                        # extent=basemap_extent,
                        reset_extent=False,
                        source=BASEMAP_SOURCE,
                        alpha=BASEMAP_ALPHA,
                        zoom=BASEMAP_ZOOM,
                        zorder=BASEMAP_ZORDER
                        )


