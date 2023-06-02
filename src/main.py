from time import time

from src.config.projectVariables import *
from src.objects.geoAxes import GeoAxes
from src.objects.geoBasemap import GeoBasemap
from src.objects.geoFigure import GeoFigure
from src.objects.geoScatterplot import GeoScatterplot
from src.utils.codeEmissions import *
from src.utils.manipulateData import *
from src.utils.simulationDirectory import *
from src.utils.unitConversion import *

simulation_folder_path = createSimulationFolder()
print(f"Created simulation output folder: {simulation_folder_path}")

tracker = initializeCarbonTracker(simulation_folder_path)
print("Initialized carbon tracker for the running code.")

tracker.start()
print("Started tracking.")

df = importFromCSV(input_columns)
print(f"Snapshots will be saved in {FILE_FORMAT} format under the name: {location_name}.")

gdf = geoDataFrameFromDataFrame(df, input_CRS)
print(f"Data obtained in CRS: {input_CRS.name}")

gdf.to_crs(output_CRS)
print(f"Reprojecting to: {output_CRS.name}")

fig = GeoFigure()
print("Initializing figure...")

ax = GeoAxes(fig, gdf)
print("Initializing axes...")

sc = GeoScatterplot(ax)
print("Initializing scatter plot...")

cx = GeoBasemap()
print("Initializing basemap...")

cx.addBasemapFromGeoDataFrame(ax, gdf)
print("Adding basemap to axes...")

for timestep in gdf['timestep'].sort_values().unique():
    start_time = time()
    timestep_gdf = gdf[gdf['timestep'] == timestep]
    sc.updateFromGeoDataFrame(timestep_gdf)
    end_time = time()  # Stop measuring the time
    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    # Print the elapsed time in seconds
    print(f"\n-= Snapshot {timestep} =-")
    print(f"Generation time: {elapsed_time:.2f} seconds")

    file_size_bytes = saveSnapshot(simulation_folder_path, timestep)
    file_size, unit = convertFileSize(file_size_bytes)
    print(f"File size: {file_size:.2f} {unit}")

# Step 7: Display a message indicating the snapshots have been saved
print("Snapshots saved successfully.")
codeEmissions: float = tracker.stop()
print(f"CO2eq emissions induced by code: {codeEmissions} kg")

# Add some prints yeah. But allow them to be turned off altogether. Perhaps seperate functions into stuff like the file size truncator.
