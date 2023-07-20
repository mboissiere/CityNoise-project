"""
This file gathers constants (written in UPPER_SNAKE_CASE) to be called in the importing of an input CSV file.
It is possible to modify them here, but in normal execution shouldn't need to happen too often.
"""
import os

# Path from the FOLDER WHERE manipulateData IS RUN to the data folder, where (potentially multiple) CSVs can be found.
PATH_TO_DATA = os.path.join('..', 'data')

# Name of the import of interest.
FILE_NAME_FROM_DATA = "traffic_data.csv"

# Constructed file path to the traffic data CSV file
TRAFFIC_DATA_PATH = os.path.join(PATH_TO_DATA, FILE_NAME_FROM_DATA)

# Name of the CSV column that holds timestep data.
TIMESTEP_COLUMN = "timestep"

# Type of the data in the timestep column. It is recommended to use Int64 to avoid errors at long timesteps.
TIMESTEP_TYPE = 'Int64'

# Name of the CSV column that holds longitude data.
LONGITUDE_COLUMN = "longitude"

# Type of the data in the longitude column.
# todo: Further code solidification could check it is a correct Longitude instead of a float, but non-urgent for now.
LONGITUDE_TYPE = float

# Name of the CSV column that holds latitude data.
LATITUDE_COLUMN = "latitude"

# Type of the data in the latitude column.
# todo: Further code solidification could check it is a correct Latitude instead of a float, but non-urgent for now.
LATITUDE_TYPE = float

# Name of the CSV column that holds geometry data.
GEOMETRY_COLUMN = "geometry"
