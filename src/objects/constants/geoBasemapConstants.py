"""
This file gathers constants (written in UPPER_SNAKE_CASE) to be called in the initialization of a ctx basemap.
It is possible to modify them here, but in normal execution shouldn't need to happen too often.
"""
import contextily as ctx

# The source for the basemap, in the background of the plot
BASEMAP_SOURCE = ctx.providers.OpenStreetMap.Mapnik

# The value for transparency of the basemap, between 0 and 1.
BASEMAP_ALPHA = 1

# Level of detail of the basemap : 18 is max, below 12 is hard to read, but above 16 is too long to compute
BASEMAP_ZOOM = 14
