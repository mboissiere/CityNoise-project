import geopandas
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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
        # print(f"Scatter gdf: {gdf}") NB : honestly, not optimized...
        self.ax = gdf.plot(color=SCATTER_COLOR,
                           marker=SCATTER_MARKER,
                           markersize=SCATTER_MARKERSIZE,
                           edgecolor=SCATTER_EDGECOLOR,
                           linewidth=SCATTER_LINEWIDTH,
                           zorder=SCATTER_ZORDER
                           )

    '''PONCER:
    - KDE avec fill et vmin/vmax qui marchent bien
    - 2D histogram pour le truc dynamique qui peut être rapide, quitte à ce que ce soit un project variable
    de choisir entre les deux modélisations
    - proposition de newt :d onner le nombre de bins sur histogramme c'est donner la résolution.
    pour une visualization bien, se poser la question de quelle valeur à donner
    bins : façon de subdiviser sur les côtés les points de l'histogramme
    - mesh grid avec les routes de sodermalm ?'''

    def createKDEPlotFromGeoDataFrame(self,
                                      gdf: geopandas.GeoDataFrame,
                                      column: str
                                      # column_max: float
                                      ):
        sns.kdeplot(x=gdf.geometry.x,  # ah ptn le nom de la colonne
                    y=gdf.geometry.y,
                    weights=gdf[column],
                    cmap=COLORMAP,
                    ax=self.ax,
                    # zorder=KDE_ZORDER
                    shade=True,
                    alpha=KDE_ALPHA,
                    shade_lowest=False,
                    cbar=True,
                    # cbar_ax=self.ax, nope, wonky, but would be nice to exert some more control
                    bw_method="silverman",
                    # vmin=0,  # doesn't seem to work, create a colorbar seperately?
                    # vmax=column_max
                    cbar_kws={'shrink': COLORBAR_SHRINK}
                    )

        # NB:  might work, but might just be extremely long..
        # KDEmap could be maybe useful but only at the end of the computation, as a bonus after the animation like CSV

        # self.ax = kde_ax
        # plt.colorbar(kde_ax.collections[0], ax=kde_ax)
        # print(f"KDE gdf: {gdf}")

        # try seaborn again
        # KJBHdskjhdsliuvhdsovhfidshi use geoplot maybe

        '''self.ax = gdf.plot(column=column,
                           # x=gdf.geometry.x,
                           # y=gdf.geometry.y,
                           kind="kde",
                           cmap=COLORMAP,
                           # legend=True,
                           ax=self.ax,
                           zorder=2
                           )'''

    # NB : should explain seaborn choice because numpy exists too. uh.
    # apparently its good for working with pandas dataframes ! wow im so good at architecture eh
    # totally just wasnt the first thing that popped up on stackoverflow (but i mean, justifiably then eh)
    def createHistogramPlotFromGeoDataFrame(self, gdf: geopandas.GeoDataFrame, column: str):
        x = gdf.geometry.x
        y = gdf.geometry.y
        weights = gdf[column]

        # Manually compute the bins based on your data
        x_min, x_max = x.min(), x.max()
        y_min, y_max = y.min(), y.max()
        length = x_max - x_min
        height = y_max - y_min
        length_over_height_ratio = length // height
        x_bins = int(length_over_height_ratio * HISTOGRAM_YBINS)
        y_bins = HISTOGRAM_YBINS
        # x_bins = np.linspace(x_min, x_max, num=HISTOGRAM_XBINS)  # Adjust the number of bins as needed
        # y_bins = np.linspace(y_min, y_max, num=HISTOGRAM_YBINS)

        # Plot the 2D histogram using sns.histplot
        sns.histplot(x=x, y=y, weights=weights, bins=[x_bins, y_bins], cmap=COLORMAP, cbar=True,
                     cbar_kws={'shrink': COLORBAR_SHRINK}, zorder=HISTOGRAM_ZORDER, alpha=HISTOGRAM_ALPHA)

        # nb : Automated estimation of the number of bins is not supported for weighted data with sns.histplot
        # but if, like Paul says, I want to explore manual bin setting, then consider using sns.histplot directly?

    def createHeatMapFromGeoDataFrame(self, gdf: geopandas.GeoDataFrame, column: str):
        # TODO: very probably adapt for multiple columns if I don't do CO2eq
        colormap = sns.color_palette(COLORMAP, as_cmap=True)
        colormap.set_under(alpha=0.0)
        sns.heatmap(gdf[column],
                    cmap=colormap,
                    # cbar_kws={"shrink": 0.7, "vmin": 0, "vmax": 100}
                    alpha=HEATMAP_ALPHA,
                    vmin=0,  # np.nextafter(0, 1)
                    ax=self.ax
                    )

        # apparently heatmap is not at all what i need ! but in fact should try a 2D histogram.

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
                        zoom=BASEMAP_ZOOM,
                        zorder=BASEMAP_ZORDER
                        )
