import geopandas
import matplotlib

from src.objects.constants.geoBasemapConstants import *


class GeoBasemap(ctx.Contextily):
    # TODO: use a constructor architecture, it just seems better.
    def __init__(self, gdf: geopandas.GeoDataFrame, *args, **kwargs):
        if 'crs' not in kwargs:
            kwargs['crs'] = gdf.crs
        if 'source' not in kwargs:
            kwargs['source'] = BASEMAP_SOURCE
        if 'alpha' not in kwargs:
            kwargs['alpha'] = BASEMAP_ALPHA
        if 'zoom' not in kwargs:
            kwargs['zoom'] = BASEMAP_ZOOM
        super().__init(*args, **kwargs)

    def addBasemapToAxes(self, ax: matplotlib.axes.Axes):
        self.add_basemap(ax)
