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

accumulation_df = initializeAccumulationDataFrame(df, input_columns)
print(f"Initialized accumulation dataframes for columns : {input_columns}")

gdf = geoDataFrameFromDataFrame(df, input_CRS)
accumulation_gdf = geoDataFrameFromDataFrame(accumulation_df, input_CRS)
print(f"Data obtained in CRS: {input_CRS.name}")

gdf.to_crs(output_CRS)
accumulation_gdf.to_crs(output_CRS)
print(f"Re-projecting to: {output_CRS.name}")

fig = GeoFigure()
print("Initializing figure and axes...")

indexGeoDataFrameWithGeometry(accumulation_gdf)
print("Re-indexing accumulation geo-dataframe using longitude and latitude...")

for timestep in gdf['timestep'].sort_values().unique():
    start_time = time()

    '''timestep_gdf = obtainGeoDataFromTimeStep(gdf=gdf,
                                             timestep=timestep,
                                             columns_of_interest=input_columns
                                             )'''
    timestep_gdf = gdf[gdf[TIMESTEP_COLUMN] == timestep]
    fig.createScatterPlotFromGeoDataFrame(timestep_gdf)
    fig.addBasemapFromGeoDataFrame(timestep_gdf)
    fig.adjustAxesFromGeoDataFrame(gdf)
    print("-= Before =-")
    print(timestep_gdf)
    indexGeoDataFrameWithGeometry(timestep_gdf)
    print("-= After =-")
    print(timestep_gdf)
    print("-= Before =-")
    print(accumulation_gdf)
    addAccumulationDataFromGeoDataFrame(accumulation_gdf, timestep_gdf, input_columns)
    print("-= After =-")
    print(accumulation_gdf)
    print(accumulation_gdf['accumulated_CO2'].sort_values())
    # Note for tomorrow : for now I see no other way than to create a np meshgrid.
    # Seaborn doesn't seem to recognize geometry when plotting.
    # OR try geopandas mapping functions directly : https://geopandas.org/en/stable/docs/user_guide/mapping.html
    # Before giving up (although controlling meshgrid could turn out to be good), try KDE plot
    # and options in "Pandas plots" section of URL
    # Good example of KDEplot and pointplot mixing :
    # https://residentmario.github.io/geoplot/gallery/plot_boston_airbnb_kde.html
    # Investigate geoplot as a module : https://residentmario.github.io/geoplot/
    # (perhaps make several implementations? idk)
    fig.createHeatMapFromGeoDataFrame(accumulation_gdf, 'accumulated_CO2')  # to generalize

    end_time = time()

    elapsed_time = end_time - start_time
    print(f"\n-= Snapshot {timestep} =-")
    print(f"Generation time: {elapsed_time:.2f} seconds")

    file_size_bytes = saveSnapshot(simulation_folder_path, timestep)
    file_size, file_size_unit = convertFileSize(file_size_bytes)
    print(f"File size: {file_size:.2f} {file_size_unit}")

print("\nSnapshots saved.")

simulated_time_seconds = simulatedTimeFromGeoDataFrame(gdf)
simulated_time, time_unit = convertTime(simulated_time_seconds)
print(f"Successfully simulated {simulated_time:.2f} {time_unit} of traffic in {location_name}.\n")

video_name = f"{location_name}_{simulated_time:.2f}{time_unit}.{VIDEO_FILE_FORMAT}"
assembleVideo(simulation_folder_path, video_name)
print(f"\nGenerated video under filename: {video_name}")

if codecarbon_enabled:
    codeEmissions: float = tracker.stop()
    print(f"CO2eq emissions induced by code: {codeEmissions} kg")
