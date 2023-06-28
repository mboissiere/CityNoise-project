"""
This file gathers constants (written in UPPER_SNAKE_CASE) to be called in the initialization of a pyplot figure.
It is possible to modify them here, but in normal execution shouldn't need to happen too often.
"""

import contextily as ctx

# todo: an idea could be to actually base it on the plot, just like I do with histogram bin size...
# actually, THIS should be based final gdf extent, and pixel size should be based on it as well...
# The horizontal figure size of the plot
FIGURE_SIZE_X = 100

# The vertical figure size of the plot
FIGURE_SIZE_Y = 100

# If there are several subplots, the number of rows in the grid that contains them. Should be just the one here.
SUBPLOT_NUMBER_ROWS = 1

# If there are several subplots, the number of columns in the grid that contains them. Should be just the one here.
SUBPLOT_NUMBER_COLUMNS = 1

# If there are several subplots, the index of our subplot of interest.
SUBPLOT_INDEX = 1

# Indicates whether or not axes should be displayed.
SHOW_AXES = True

# Resizing of axes - "auto" by default, can be set to 'equal' if a square aspect ratio is desired.
AXES_ASPECT_MODE = "auto"

# Size of the points or markers in a scatter plot, if it is chosen constant
SCATTER_MARKERSIZE = 2

# Color of the points in a scatter plot
SCATTER_COLOR = "white"

# Choice of marker in a scatter plot
SCATTER_MARKER = 'o'

# Choice of the markers' edge colors in a scatter plot
SCATTER_EDGECOLOR = "black"

# Choice of the markers' edge size in a scatter plot
SCATTER_LINEWIDTH = 0.5

# Order of the scatter plot in the z-plane : the higher the number, the closer to the front
SCATTER_ZORDER = 3

# Car icon, if one wants to make a scatter plot with car markers
CAR_ICON_PATH = "../view/car_16px.png"

# The source for the basemap, in the background of the plot
BASEMAP_SOURCE = ctx.providers.OpenStreetMap.Mapnik

# The value for transparency of the basemap, between 0 and 1.
BASEMAP_ALPHA = 1

# Level of detail of the basemap : 18 is max, below 12 is hard to read, but above 16 is too long to compute
BASEMAP_ZOOM = 14
# 16 is pretty mode, I think 17 is impossible. Perhaps 14 or 15 would be balanced mode, and 12 fast mode.
# There is a big difference between 14 and 15 imo, perhaps 17, 15 and 13? Yea thats good
# There is no level of zooming where text is readable, sadly.
# Perhaps add a certain feature: time estimator, in minutes/hours
# from an interpolation of the first 5 generations and total number of snapshots

# Order of the basemap in the z-plane : the higher the number, the closer to the front
BASEMAP_ZORDER = 1

# The colormap most appropriate for visualization
COLORMAP = "YlOrRd"

# The value for transparency of the heatmap, between 0 and 1.
KDE_ALPHA = 0.5

# Order of the KDE plot in the z-plane : the higher the number, the closer to the front
KDE_ZORDER = 2

# Order of the 2D histogram in the z-plane : the higher the number, the closer to the front
HISTOGRAM_ZORDER = 2

# Number of bins in the x space for histogram (YEAH OK THIS ISNT CLEAR/USEFUL COMPARED TO THE VARIABLE ILL CHANGE MY MIND LATER)
HISTOGRAM_XBINS = 100

# TODO: make a custom "auto" setting that just uses figure size to determine something ok

# same for y bro
# ok but honestly this should be a project variable its so important and probably could be changed
HISTOGRAM_YBINS = 100

HISTOGRAM_NBINS = 100

HISTOGRAM_ALPHA = 0.75

# How much the colorbar should be shrinked, for purely visualization purposes.
COLORBAR_SHRINK = 0.5
