"""
This module performs conversion of units commonly encountered in the simulation.

It is important to keep in check the base unit that is exported from the CSV!
So far, instantaneous emissions are assumed to be in grams, but that could always change.
TODO: More advanced versions could perhaps read this data from the CSV itself.

TODO: I could also make object oriented programming with pint's PhysicalQuantity objects but this is not a priority
(LMAO HELP THIS IS JUST FOR A DISPLAY, WHY DO I DO THIS, STOP)
"""
from src.constants.unitConversionConstants import *
from pandas import DataFrame


def convertFloat(value: float, units_list: list, base: int):
    """
    The very basics of a unit conversion function that converts a single output.
    Note that input_float will be modified, function does NOT act on a copy.

    :param value: The value to be converted.
    :param units_list: A list of strings containing names of units in the system of interest.
    :param base: The base of the unit conversion, such that in the units list, ratio between neighbors is the base.
    :return: Converted float and its most suited unit for display.
    :rtype tuple:
    """
    i = 0
    while value >= base and i < len(units_list):
        i += 1
        value /= base
    unit = units_list[i]
    return value, unit


def convertFileSize(file_size):
    """
    Convert a filesize in bytes to higher units for readability.

    :param float file_size: Initial size of the file, in bytes.
    :return: Converted file size and its most suited unit for display.
    :rtype tuple(float, str):
    """
    convertFloat(file_size, FILE_SIZE_UNITS, FILE_SIZE_BASE)


def convertDataFrame(dataframe: DataFrame, key: str, max_value: float, units_list: list, base: int):
    """
    The very basics of a unit conversion function that converts a dataframe, using a maximum value for reference.
    Note that the dataframe and max value will be modified, function does NOT act on a copy.

    Said maximum value defines the maximum of what we care about in data visualization, but it is not necessarily the
    maximum value of the column (it could be, for example, a maximum aggregated over time in a dynamic plot).

    :param dataframe: The dataframe containing the data we would like to convert.
    :param key: The name of the column of interest, such that dataframe[key] calls it.
    :param max_value: A maximum value that will bound our visualization of the data.
    :param units_list: A list of strings containing names of units in the system of interest.
    :param base: The base of the unit conversion, such that in the units list, ratio between neighbors is the base.
    :return: Converted maximum value and its most suited unit for display
    :rtype tuple(float, str):
    """

    i = 0
    while max_value >= base and i < len(units_list):
        i += 1
        dataframe[key] /= base
        max_value /= base
    unit = units_list[i]
    return max_value, unit


def convertEmissions(dataframe: DataFrame, gas_type: str, max_value: float):
    """
    Receives a column from a Pandas DataFrame (or GeoPandas GeoDataFrame) with emission data, assumed to be in grams,
    and converts it to higher units for readability while assuming it won't exceed a certain value.

    Caution! This function would need to be adapted if the data is anything other than grams.
    TODO: Generalize the function even more to allow different entry units.

    Caution! Minimum is assumed to be zero.
    TODO: Allow minimum to also be considered in conversion, or at least raise an exception.

    :param dataframe: The dataframe containing the data we would like to convert.
    :param gas_type: The name of the gas of interest.
    :param max_value: A maximum value that will bound our visualization of the data.
    :return: Converted maximum value and its most suited unit for display
    :rtype tuple(float, str):
    """
    convertDataFrame(dataframe, gas_type, max_value, WEIGHT_KILO_UNITS, KILO_UNIT_BASE)
