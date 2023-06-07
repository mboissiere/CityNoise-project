import logging
from time import time

from src.config.projectVariables import *
from src.objects.geoFigure import *
from src.utils.codeEmissions import *
from src.utils.manipulateData import *
from src.utils.simulationDirectory import *
from src.utils.unitConversion import *

logging.getLogger("moviepy").setLevel(logging.WARNING)
logging.getLogger("codecarbon").setLevel(logging.WARNING)
print("Disabled unimportant logging prints.")

# perhaps a variable "log carbon"

simulation_folder_path = createSimulationFolder()
print(f"Created simulation output folder: {simulation_folder_path}")

if codecarbon_enabled:
    tracker = initializeCarbonTracker(simulation_folder_path)
    print("Initialized carbon tracker for the running code.")

    tracker.start()
    print("Started tracking.")

df = importFromCSV(input_columns)
print(f"Snapshots will be saved in {IMAGE_FILE_FORMAT} format under the name: {location_name}.")

gdf = geoDataFrameFromDataFrame(df, input_CRS)
print(f"Data obtained in CRS: {input_CRS.name}")

gdf.to_crs(output_CRS)
print(f"Re-projecting to: {output_CRS.name}")

accumulation_gdf = initializeAccumulationGeoDataFrame(gdf, input_columns, output_CRS)
print(f"Initialized accumulation dataframes for columns : {input_columns}")

fig = GeoFigure()
print("Initializing figure and axes...")

CO2_max = getPointMaximumFromGeoDataFrame(gdf=gdf, column='CO2')

# indexGeoDataFrameWithGeometry(accumulation_gdf)
# print("Re-indexing accumulation geo-dataframe using longitude and latitude...")
# print(accumulation_gdf.columns)

print("\nInitialization complete! Beginning simulation loop.")
for timestep in gdf['timestep'].sort_values().unique():
    # todo: measure global time as well as individual. also, count saving of snapshot
    start_time = time()

    '''timestep_gdf = obtainGeoDataFromTimeStep(gdf=gdf,
                                             timestep=timestep,
                                             columns_of_interest=input_columns
                                             )'''
    timestep_gdf = gdf[gdf[TIMESTEP_COLUMN] == timestep]
    fig.createScatterPlotFromGeoDataFrame(timestep_gdf)
    fig.addBasemapFromGeoDataFrame(timestep_gdf)
    fig.adjustAxesFromGeoDataFrame(gdf)
    accumulation_gdf = addAccumulationDataFromGeoDataFrame(accumulation_gdf, timestep_gdf, input_columns)

    if plot_type == "KDE":
        fig.createKDEPlotFromGeoDataFrame(accumulation_gdf, 'accumulated_CO2')  # to generalize
    elif plot_type == "Histogram":
        fig.createHistogramPlotFromGeoDataFrame(accumulation_gdf, 'accumulated_CO2')

    end_time = time()

    elapsed_time = end_time - start_time
    print(f"\n-= Snapshot {timestep} =-")
    print(f"Generation time: {elapsed_time:.2f} seconds")

    # todo: refactor savesnapshot honestly its weird for it to include file size
    file_size_bytes = saveSnapshot(simulation_folder_path, timestep)
    file_size, file_size_unit = convertFileSize(file_size_bytes)
    print(f"File size: {file_size:.2f} {file_size_unit}")

print(f"\n{plot_type} snapshots saved.")

fig.createKDEPlotFromGeoDataFrame(accumulation_gdf, 'accumulated_CO2')
file_size_bytes = saveSnapshot(simulation_folder_path, timestep)
file_size, file_size_unit = convertFileSize(file_size_bytes)
print(f"\nEnd state KDE snapshot saved ({file_size:.2f} {file_size_unit})")

# To comment
csv_filename = os.path.join(simulation_folder_path, 'accumulated_CO2.csv')
accumulation_gdf.to_csv(csv_filename)

simulated_time_seconds = getSimulatedTimeFromGeoDataFrame(gdf)
simulated_time, time_unit = convertTime(simulated_time_seconds)
print(f"Successfully simulated {simulated_time:.2f} {time_unit} of traffic in {location_name}.\n")

video_name = f"{location_name}_{simulated_time:.2f}{time_unit}.{VIDEO_FILE_FORMAT}"
assembleVideo(simulation_folder_path, video_name)
print(f"\nGenerated video under filename: {video_name}")

if codecarbon_enabled:
    codeEmissions: float = tracker.stop()
    print(f"CO2eq emissions induced by code: {codeEmissions} kg")
