"""
This module configures the output folder of a simulation, and contains helper functions for display if needed.
"""
import os
import matplotlib.pyplot as plt
from datetime import datetime
from src.config.projectVariables import snapshot_name
from src.constants.simulationDirectoryConstants import *


def createSimulationFolder():
    """
    Creates a folder in which to save screenshots from the simulation.
    Sorts it using date & time of simulation launch, as to not clog up workspace.

    :return: The path of the folder where simulation files will be saved.
    :rtype str:
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


def saveSnapshot(simulation_folder_path:str, timestep:int):
    """
    Saves the current figure in pyplot as an image.

    :param simulation_folder_path: Path of the simulation folder where snapshots will be saved.
    :param timestep: Timestep currently represented by the snapshot being saved.
    :return: None
    """
    filename = f'{simulation_folder_path}/{snapshot_name}_{timestep}.{FILE_FORMAT}'
    plt.savefig(fname=filename, dpi=DPI, bbox_inches=BBOX_SETTINGS)
