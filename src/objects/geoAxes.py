import matplotlib.pyplot as plt

from src.objects.constants.geoAxesConstants import *


class GeoAxes(plt.Axes):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_aspect(AXES_ASPECT_MODE)
        if not SHOW_AXES:
            self.set_axis_off()

    def setBoundsFromGeoDataFrame(self, gdf):
        min_lon, min_lat, max_lon, max_lat = gdf.total_bounds
        self.set_xlim(min_lon, max_lon)
        self.set_ylim(min_lat, max_lat)
