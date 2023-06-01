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

# Size of the points or markers in a scatter plot
SCATTER_POINT_SIZE = 1

# Car icon, purely aesthetic
CAR_ICON_PATH = "../view/car_16px.png"

# Resizing of axes - can be set to 'equal' if a square aspect ratio is desired.
AXES_ASPECT_MODE = 'auto'

# The source for the basemap, in the background of the plot
BASEMAP_SOURCE = ctx.providers.OpenStreetMap.Mapnik
