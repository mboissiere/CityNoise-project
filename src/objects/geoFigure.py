import matplotlib.pyplot as plt

from src.objects.constants.geoFigureConstants import *


class GeoFigure(plt.Figure):
    def __init__(self, *args, **kwargs):
        if 'figsize' not in kwargs:
            kwargs['figsize'] = (FIGURE_SIZE_X, FIGURE_SIZE_Y)
        super().__init__(*args, **kwargs)
