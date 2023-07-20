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
        self.ax.set_title("Air pollution simulation in Södermalm")  # to change
        self.ax.set_xlabel("Longitude")
        self.ax.set_ylabel("Latitude")

    '''def addColorbar(self, colorbar_min, colorbar_max):
        cmap = plt.get_cmap(COLORMAP)
        norm = mcolors.Normalize(vmin=colorbar_min, vmax=colorbar_max)
        scalar_map = plt.cm.ScalarMappable(cmap=cmap, norm=norm)

        # Calculate the position of the colorbar
        colorbar_width = 0.03  # Adjust the width as needed
        colorbar_height = 0.7 * self.fig.get_figheight()  # Adjust the height as needed
        colorbar_x = 0.92  # Adjust the x-coordinate as needed
        colorbar_y = 0.15 + (0.7 * (1 - colorbar_height / self.fig.get_figheight())) / 2

        cax = self.fig.add_axes([colorbar_x, colorbar_y, colorbar_width, colorbar_height])
        colorbar = self.fig.colorbar(scalar_map, cax=cax)
        colorbar.set_label('Colorbar Label')'''

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
        x = gdf.geometry.x
        y = gdf.geometry.y
        weights = gdf[column]

        # Manually compute the bins based on your data
        x_min, x_max = x.min(), x.max()
        y_min, y_max = y.min(), y.max()
        length = x_max - x_min
        height = y_max - y_min
        length_over_height_ratio = length // height
        x_bins = HISTOGRAM_XBINS  # int(length_over_height_ratio * HISTOGRAM_YBINS)
        y_bins = HISTOGRAM_YBINS

        # x_bins = np.linspace(x_min, x_max, num=HISTOGRAM_XBINS)  # Adjust the number of bins as needed
        # y_bins = np.linspace(y_min, y_max, num=HISTOGRAM_YBINS)

        # Plot the 2D histogram using sns.histplot
        # it's possible that seaborn is actually annoying and i should manually plot it with numpy

        # Or perhaps, imitate the structure of my v2, where I initialize a plot with sc = ...
        # might even initialize with tne end state since i need it for information

        # curious : switching from sns.histplot to self.ax = ... seems to change values? cbar goes above 3 now?
        # MAKE TESTS. CHECK THAT THIS ACTUALLY IS CORRECT.
        # edit: euh non mdr j'ai juste réduit les pixels c juste ca
        # AND CONSIDER. GEOPLOT.
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
        '''cbar = plt.colorbar(ax.collections[0], ax=ax)
        cbar.set_ticks([0, column_max])
        cbar.set_clim(0, column_max)'''

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

    # see if there isn't a way for me to initialize basemap and axes once, and then act on self.ax, and i've just
    # been doing it wrong
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


# Consider mastering pyplot's arguments (Pierre's book?) instead of relying on seaborn
# which facilitates some work but also locks me (e.g. annoying to set basemap extent, to do histogram interpolation)


'''Consider doing interpolation for a continuous view of the 2D histogram:

# Create the seaborn histogram plot
sns.histplot(data)

# Get the current figure and axis from the plot
fig = plt.gcf()
ax = plt.gca()

# Clear the plot
ax.clear()

# Apply interpolation using imshow and set the desired interpolation method
im = ax.imshow(data, cmap='hot', interpolation='bilinear')
'''
