import matplotlib

from src.objects.constants.geoScatterplotConstants import *


# TODO: comment this

class GeoScatterplot(matplotlib.collections.PathCollection):
    def __init__(self, ax: matplotlib.axes.Axes):
        super().__init__(paths=[], sizes=[], offsets=[], transOffset=ax.transData)
        ax.add_collection(self)
        self._marker.set_marker(SCATTER_MARKER)
        self._facecolors = SCATTER_COLOR
        # TODO: constant size is assumed, perhaps later size will be variable?
        # Same thing with vehicle appearance, color... Could change...
        self.set_sizes(SCATTER_MARKERSIZE)
        self.set_edgecolor(SCATTER_EDGECOLORS)

    def updateFromGeoDataFrame(self, gdf):
        x_column = gdf.geometry.x
        y_column = gdf.geometry.y
        self.set_offsets(list(zip(x_column, y_column)))
