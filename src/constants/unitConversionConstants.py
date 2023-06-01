"""
This file gathers constants_2 (written in UPPER_SNAKE_CASE) and variables (written in lower_snake_case) to be called in
the unit conversion function (see utils2).
"""

# Notations for standard file size units.
FILE_SIZE_UNITS = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB']

# Base for file size unit conversion
FILE_SIZE_BASE = 1024

# Notations for standard weight units (gas emissions literature usually only cares about powers of 1000).
WEIGHT_KILO_UNITS = ['g', 'kg', 't', 'kt', 'Mt', 'Gt']

# Base for standard conversion by a thousand.
KILO_UNIT_BASE = 1000
