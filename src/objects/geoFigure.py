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
                           edgecolor=SCATTER_EDGECOLOR,
                           linewidth=SCATTER_LINEWIDTH
                           )

    def createKDEPlotFromGeoDataFrame(self, gdf: geopandas.GeoDataFrame, column: str):
        kde_ax = sns.kdeplot(data=gdf[column],
                             cmap=COLORMAP,
                             ax=self.ax,
                             shade=True,
                             shade_lowest=False,
                             cbar=True
                             )
        self.ax = kde_ax
        # plt.colorbar(kde_ax.collections[0], ax=kde_ax)
        '''self.ax = gdf.plot(column=column,
                           kind="kde",
                           cmap=COLORMAP
                           )'''

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
        # Note for tomorrow : for now I see no other way than to create a np meshgrid.
        # Seaborn doesn't seem to recognize geometry when plotting.
        # OR try geopandas mapping functions directly : https://geopandas.org/en/stable/docs/user_guide/mapping.html

    # Before giving up (although controlling meshgrid could turn out to be good), try KDE plot
    # and options in "Pandas plots" section of URL
    # Good example of KDEplot and pointplot mixing :
    # https://residentmario.github.io/geoplot/gallery/plot_boston_airbnb_kde.html
    # Investigate geoplot as a module : https://residentmario.github.io/geoplot/
    # (perhaps make several implementations? idk)

    # TODO: consider geoplot in a potential refactoring, but not sure if needed rn

    def addBasemapFromGeoDataFrame(self, gdf: geopandas.GeoDataFrame):
        # basemap_extent = gdf.total_bounds
        ctx.add_basemap(self.ax,
                        crs=gdf.crs,
                        # extent=basemap_extent,
                        source=BASEMAP_SOURCE,
                        alpha=BASEMAP_ALPHA,
                        zoom=BASEMAP_ZOOM)
