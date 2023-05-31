from geopandas import GeoDataFrame
from pyproj import CRS


def reprojectEPSG(gdf, input_epsg, output_epsg):
    """
    This function takes in a GeoDataFrame that has been mapped at a given CRS (represented by its EPSG identifier)
    and reprojects it to a different CRS (also represented by its EPSG identifier).
    This function acts directly on the GeoDataFrame and modifies it.

    TODO: This assumes EPSG coding, improvements on this method could perhaps allow different nomenclature.

    :param GeoDataFrame gdf: The GeoDataFrame to be reprojected.
    :param int input_epsg: The EPSG identifier of the initial CRS.
    :param int output_epsg: The EPSG identifier of the desired CRS.
    :return: None
    """
    input_crs = CRS.from_epsg(input_epsg)
    output_crs = CRS.from_epsg(output_epsg)
    gdf.to_crs(output_crs)
