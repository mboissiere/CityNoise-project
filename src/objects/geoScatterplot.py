from src.objects.constants.geoScatterplotConstants import *


# TODO: comment this

class GeoScatterplot:
    def __init__(self, ax, gdf):
        self.ax = ax
        self.scatter = self.ax.scatter(gdf.geometry.x,
                                       gdf.geometry.y,
                                       c=SCATTER_COLOR,
                                       s=SCATTER_SIZE,
                                       marker=SCATTER_MARKER,
                                       edgecolor=SCATTER_EDGECOLOR
                                       )

    def updateFromGeoDataFrame(self, gdf):
        self.scatter.set_offsets(list(zip(gdf.geometry.x, gdf.geometry.y)))
