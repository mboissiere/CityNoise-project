"""
This file gathers all project variables (written in lower_snake_case) that play a role in the simulation configuration.
"""
from pyproj import CRS

from src.config.projectConstants import *

# Can be made to change depending on neighborhood studied.
location_name = "sodermalm"

# Name of the import of interest.
data_path = "fcdgeo_2h.csv"

# Name of the paper presenting the model currently in use.
model_name = "Coelho2006"

# Names of columns that will be imported and studied. Timestep, longitude and latitude are already imported by default.
input_columns = ['CO2']

# EPSG identifier of the CRS used in the creation of the model's CSV
input_CRS = CRS.from_epsg(EPSG_WORLD_GEODESIC_SYSTEM)

# EPSG identifier of the output CRS desired in case of reprojection
output_CRS = CRS.from_epsg(EPSG_PSEUDO_MERCATOR)

# Enable/disable code's tracking of emissions by codecarbon
codecarbon_enabled = False

plot_type = "Histogram"  # "Histogram" or "KDE" (NB : KDE is actually deprecated)
