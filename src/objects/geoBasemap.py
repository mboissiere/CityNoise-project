import geopandas
import matplotlib

from src.objects.constants.geoBasemapConstants import *


class GeoBasemap:
    @staticmethod
    def addBasemapFromGeoDataFrame(ax: matplotlib.axes.Axes, gdf: geopandas.GeoDataFrame):
        basemap_extent = gdf.total_bounds
        ctx.add_basemap(ax,
                        crs=gdf.crs,
                        extent=basemap_extent,
                        source=BASEMAP_SOURCE,
                        alpha=BASEMAP_ALPHA,
                        zoom=BASEMAP_ZOOM)
