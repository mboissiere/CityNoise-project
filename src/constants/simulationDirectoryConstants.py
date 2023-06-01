"""
This file gathers constants_2 (written in UPPER_SNAKE_CASE) to be called in the generation of an image output.
It is possible to modify them here, but in normal execution shouldn't need to happen too often.
"""

# Standard notation for an output folder, can be changed if desired.
OUTPUT_STANDARD = "../output"

# File format is jpg by default. Can be png, but be aware file sizes can get quite large for not much benefit.
FILE_FORMAT = "jpg"

# Image resolution
DPI = 300

# Argument to be parsed in plt.savefig - wraps size of bounding box around image
BBOX_SETTINGS = "tight"
