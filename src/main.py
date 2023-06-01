from time import time

import codecarbon

from src.config.projectVariables import *
from src.utils.manipulateData import *
from src.utils.simulationDirectory import *
from src.utils.simulationPlot import *
from src.utils.unitConversion import *

# Objective of version 3 :
# speed it up (there are probably redundancies)
# investigate cartopy, seems like a better route for plotting actually
# if anything, this really probably should be a heatmap, and not a scatter plot.
# maybe it's not so stupid to be able to set a t_min and t_max. that way if animation is interrupted, we can start from later on?
# it's kind of annoying actually that the blue isn't all that impressive because if a latitude and longitude isn't "exactly right" well it won't be summed...

# a numpy approach of a mesh grid could be fine, so that points would be accumulated in areas
# and also computations arent too long. apparently scipy has good content for sparse matrices.
# MIGRATE TO GITHUB BECAUSE ACTUALLY MANUAL VERSIONING IS A MESS IF I WANT TO IMPLEMENT AN IDEA TO FUNCTIONAL OR TEST

# Set snapshot names - timesteps will be added automatically

tracker = codecarbon.OfflineEmissionsTracker(country_iso_code="SWE")
tracker.start()

df = importFromCSV(input_columns)
print("Snapshots will be saved under the name:", location_name)

gdf = geoDataFrameFromDataFrame(df, input_CRS)
print(f"Data obtained from CRS: {input_CRS.name}")

gdf.to_crs(output_CRS)
print(f"Reprojecting to: {output_CRS.name}")

fig, ax = initializeFigureAndAxes(gdf)
print("Initializing figure and axes...")

sc = initializeScatterPlot(ax)
print("Initializing scatter plot...")

simulation_folder_path = createSimulationFolder()
print(f"Created simulation output folder: {simulation_folder_path}")

for timestep in gdf['timestep'].sort_values().unique():
    start_time = time()
    timestep_gdf = gdf[gdf['timestep'] == timestep]
    sc = updateScatterPlotFromGeoDataFrame(sc, ax, timestep_gdf)
    addBasemapFromCRS(ax, output_CRS)
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
