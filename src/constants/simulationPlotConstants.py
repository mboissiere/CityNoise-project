"""
This file gathers constants (written in UPPER_SNAKE_CASE) to be called in the plotting of a simulation.
It is possible to modify them here, but in normal execution shouldn't need to happen too often.
"""
import contextily as ctx

# The horizontal figure size of the plot
FIGURE_SIZE_X = 20

# The vertical figure size of the plot
FIGURE_SIZE_Y = 20

# The colormap most appropriate for visualization
COLORMAP = "YlOrRd"

# How much the colorbar should be shrinked, for purely visualization purposes.
COLORBAR_SHRINK = 0.5

# Size of the points or markers in a scatter plot, if it is chosen constant
SCATTER_MARKERSIZE = 5

# Color of the points in a scatter plot
SCATTER_COLOR = "white"

# Choice of marker in a scatter plot
SCATTER_MARKER = 'o'

# Choice of the markers' edge colors in a scatter plot
SCATTER_EDGECOLORS = "black"

# Car icon, if one wants to make a scatter plot with car markers
CAR_ICON_PATH = "../view/car_16px.png"

# Indicates whether or not axes should be displayed.
SHOW_AXES = False

# Resizing of axes - "auto" by default, can be set to 'equal' if a square aspect ratio is desired.
AXES_ASPECT_MODE = "equal"

# The source for the basemap, in the background of the plot
BASEMAP_SOURCE = ctx.providers.OpenStreetMap.Mapnik

# The value for transparency of the basemap, between 0 and 1.
BASEMAP_ALPHA = 1

# Level of detail of the basemap : 18 is max, below 12 is hard to read, but above 16 is too long to compute
BASEMAP_ZOOM = 12
