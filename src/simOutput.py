"""
This module configures the output folder of a simulation, and contains helper functions for display if needed.

Module-level functions:
- createSimulationFolder
- saveSnapshot
"""
import os
import matplotlib.pyplot as plt
from datetime import datetime
from src.constants.outputConstants import *


def createSimulationFolder():
    """
    Creates a folder in which to save screenshots from the simulation.
    Sorts it using date & time of simulation launch, as to not clog up workspace.

    :return: simulation_folder_path, string of the path that can be used in printing if needed.
    """

    # Check if "output" folder exists, and create one if it doesn't.
    if not os.path.exists(OUTPUT_STANDARD):
        os.makedirs(OUTPUT_STANDARD)
        print(f"Created '{OUTPUT_STANDARD}' folder.")

    # Get the current date and time, format it in strings.
    simulation_datetime = datetime.now()
    simulation_date = simulation_datetime.strftime("%Y-%m-%d")
    simulation_time = simulation_datetime.strftime("%H-%M-%S")

    # Create a folder with the architecture: \output\date\time
    simulation_folder_path = os.path.join(OUTPUT_STANDARD, simulation_date, simulation_time)
    os.makedirs(simulation_folder_path)
    return simulation_folder_path


def saveSnapshot(simulation_folder_path, timestep):
    """

    :param simulation_folder_path: path of the simulation folder where snapshots will be saved
    :param timestep: timestep currently represented by the snapshot being saved
    :return: None
    """
    filename = f'{simulation_folder_path}/{snapshot_name}_{timestep}.{file_format}'
    plt.savefig(fname=filename, dpi=dpi, bbox_inches=BBOX_SETTINGS)
