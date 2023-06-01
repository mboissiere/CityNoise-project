from time import time

import codecarbon

from src.config.projectVariables import *
from src.utils.manipulateData import *
from src.utils.simulationDirectory import *
from src.utils.simulationPlot import *
from src.utils.unitConversion import *

simulation_folder_path = createSimulationFolder()
print(f"Created simulation output folder: {simulation_folder_path}")

# To be isolated
tracker = codecarbon.OfflineEmissionsTracker(country_iso_code="SWE",
                                             output_dir=simulation_folder_path,
                                             output_file="kgCO2eq_emitted_by_code.csv")
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

for timestep in gdf['timestep'].sort_values().unique():
    start_time = time()
    timestep_gdf = gdf[gdf['timestep'] == timestep]
    updateScatterPlotFromGeoDataFrame(sc, timestep_gdf)
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
