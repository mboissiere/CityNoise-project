import geopandas
import matplotlib

from src.objects.constants.geoAxesConstants import *
from src.objects.geoFigure import GeoFigure


class GeoAxes(matplotlib.axes.Subplot):
    def __init__(self, fig: GeoFigure, gdf: geopandas.GeoDataFrame, *args, **kwargs):
        fig.add_subplot(self)
        self.set_aspect(AXES_ASPECT_MODE)
        if not SHOW_AXES:
            self.set_axis_off()
        min_lon, min_lat, max_lon, max_lat = gdf.total_bounds
        width = max_lon - min_lon
        height = max_lat - min_lat
        super().__init__(fig, [min_lon, min_lat, width, height], *args, **kwargs)
