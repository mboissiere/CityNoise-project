import geopandas
import matplotlib

from src.objects.constants.geoBasemapConstants import *


class GeoBasemap:
    @staticmethod
    def addBasemapFromGeoDataFrame(self, ax: matplotlib.axes.Axes, gdf: geopandas.GeoDataFrame):
        self.add_basemap(ax,
                         crs=gdf.crs,
                         extent=gdf.total_bounds,
                         source=BASEMAP_SOURCE,
                         alpha=BASEMAP_ALPHA,
                         zoom=BASEMAP_ZOOM)
