import codecarbon

from src.constants.codeEmissionsConstants import *


def initializeCarbonTracker(output_directory: str):
    """
    
    :param output_directory:
    :return:
    """
    tracker = codecarbon.OfflineEmissionsTracker(country_iso_code=COUNTRY_ISO_CODE,
                                                 output_dir=output_directory,
                                                 output_file=OUTPUT_FILE_NAME)
    return tracker
