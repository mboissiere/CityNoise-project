import geopandas
import matplotlib

from src.objects.constants.geoBasemapConstants import *


class GeoBasemap:
    @staticmethod
    def addBasemapFromGeoDataFrame(ax: matplotlib.axes.Axes, gdf: geopandas.GeoDataFrame):
        ctx.add_basemap(ax,
                        crs=gdf.crs,
                        source=BASEMAP_SOURCE,
                        alpha=BASEMAP_ALPHA,
                        zoom=BASEMAP_ZOOM)
