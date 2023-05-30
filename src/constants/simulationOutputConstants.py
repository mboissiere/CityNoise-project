"""
This file gathers constants (written in UPPER_SNAKE_CASE) and variables (written in lower_snake_case) to be called in
the generation of an image output by the program.
"""

# Standard notation for an output folder, can be changed if desired.
OUTPUT_STANDARD = "output"

# Can be made to change depending on neighborhood studied, but we're not that far in the code yet, so constant for now.
snapshot_name = "sodermalm"

# File format is jpg by default. Can be png, but be aware file sizes can get quite large for not much benefit.
file_format = "jpg"

# Image resolution
dpi = 300

# Argument to be parsed in plt.savefig - wraps size of bounding box around image
BBOX_SETTINGS = "tight"