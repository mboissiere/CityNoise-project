import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import time
from datetime import datetime
from pyproj import CRS

# Check if "output" folder exists, and create one if it doesn't
output_folder = "output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print("Created 'output' folder.")

# Get the current date and time
current_time = datetime.now()
simulation_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")

# Create a folder with the current date and time as its name
simulation_folder = os.path.join(output_folder, simulation_time)
os.makedirs(simulation_folder)
print("Created simulation folder:", simulation_folder)

# Set snapshot names - timesteps will be added automatically
snapshot_name = 'sodermalm'
print("Snapshots will be saved under the name:", snapshot_name)

# Step 1: Read the CSV file into a Pandas DataFrame, filtering out rows with N/A timesteps
# Note to self : explain Int64. int doesnt work, perhaps with 20000 etc, creats N/A
df = pd.read_csv('traffic_data.csv',
                    usecols=['timestep', 'longitude', 'latitude', 'CO2'],
                    dtype={'timestep': 'Int64', 'longitude': float, 'latitude': float, 'CO2': float}).dropna()

# KNOWING ORIGINAL CRS OF THE DATA? SPECIFY IT IN THE IMPROT
input_crs = CRS.from_epsg(4326)
print(f"Data obtained from CRS: {input_crs.name}")
#COMMENT WHAT THESE ARE EXACTLY

# Specify the CRS to be projected. Here, EPSG:3847 means pseudo-Mercator, but it can be changed.
#4814 is Stockholm
output_crs = CRS.from_epsg(4814)
print(f"Reprojecting to: {output_crs.name}")

# Step 2: Create a GeoDataFrame from the DataFrame
geometry = gpd.points_from_xy(df['longitude'], df['latitude'])
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs=input_crs)

# Reproject
gdf.to_crs(output_crs)

# Group data by latitude and longitude, and calculate the sum of CO2 values for each location
groupedCO2 = gdf.groupby(['latitude', 'longitude'])['CO2'].sum()

# Calculate the maximum CO2 pollution at a single point
max_CO2 = groupedCO2.max()

print(f"Longitudes x latitudes explored: {len(gdf['longitude'])} x  {len(gdf['latitude'])}")



# Step 3: Calculate the bounding box coordinates
min_lon, min_lat, max_lon, max_lat = gdf.total_bounds

# Adjust the CO2 unit and colorbar label based on the maximum value
# Determine the appropriate unit for the colorbar
if max_CO2 >= 1000:
    gdf['CO2'] /= 1000
    max_CO2 /= 1000
    unit = 'kilograms'
    if max_CO2 >= 1000:
        gdf['CO2'] /= 1000
        max_CO2 /= 1000
        unit = 'tons'
else:
    unit = 'grams'

# Step 5: Set up the figure and axes
fsize = 20
fig, ax = plt.subplots(figsize = (fsize,fsize))
# Explain exactly what fig and ax are ! The figure and the colorbar, subplots side to side. This is where we control the size.
ax.set_aspect('equal')
ax.set_axis_off()
ax.set_xlim(min_lon, max_lon)
ax.set_ylim(min_lat, max_lat)

# Calculate the appropriate zoom level based on the extent of the data
#zoom_level = ctx.tile._calculate_zoom(min_lat, max_lat, min_lon, max_lon)
#print(zoom_level) apparently 5 ?

# Adjust the zoom level to fit within the valid range
#zoom_level = min(zoom_level, 18)  # Set the maximum valid zoom level




# Initialize the colorbar with the maximum CO2 value
colormap = 'plasma'
scatter_size = 1
sc = ax.scatter([], [], c=[], cmap=colormap, s=scatter_size, vmin=0, vmax=max_CO2)
cbar = plt.colorbar(sc, ax=ax, label=f'CO2 Pollution ({unit})', shrink=0.5)
#shrink = 0.6 argument previously

# Step 6: Loop over each timestep and update the CO2 values
aggregated_data = gdf.groupby(['longitude', 'latitude'])['CO2'].cumsum()

# Loop over each timestep and update the scatter plot
for timestep in df['timestep'].unique():
    start_time = time.time()  # Start measuring the time
    #idk what these do, try uncommenting to see if it really changes stuff?

    # Filter data for the current timestep and aggregate CO2 values
    timestep_data = gdf[gdf['timestep'] <= timestep] #THIS IS WHY ITS TAKING AGES
    aggregated_values = aggregated_data[timestep_data.index]

    sc = ax.scatter(
        timestep_data.geometry.x,
        timestep_data.geometry.y,
        c=aggregated_values,
        cmap=colormap,
        s=scatter_size,
        vmin=0,
        vmax=max_CO2,
    )
    # Add the basemap with the calculated zoom level
    # ctx.add_basemap(ax, crs=gdf.crs, source=ctx.providers.OpenStreetMap.Mapnik, alpha=0.5, zoom=zoom_level)
    ctx.add_basemap(ax, crs=gdf.crs, source=ctx.providers.OpenStreetMap.Mapnik)
    # additional unspecifies arguments : alpha=1, zoom=14
    #zoom provides a balance between low and high detail. Starting at 12 for reasonable info, 18 is max but takes huge amounts to generate.
    # To have an idea : 12 zoom takes a few seconds to generate, has abt 900 kb without further compression, is blurry.
    # 16 zoom takes
    # Explain this funky alpha value
    #cbar.ax.set_ylabel(f'CO2 Pollution ({unit})')
    file_format = "jpg"
    # Explain advantages and disadvantages of png/jpg
    filename = f'{simulation_folder}/{snapshot_name}_{timestep}.{file_format}'
    plt.savefig(fname=filename, dpi=300, bbox_inches='tight')
    end_time = time.time()  # Stop measuring the time
    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    # Print the elapsed time in seconds
    print(f"\n-= Snapshot {timestep} =-")
    print(f"Generation time: {elapsed_time:.2f} seconds")

    # Get the size of the file in bytes
    file_size = os.path.getsize(filename)

    # Convert the file size to KB or MB
    if file_size < 1024:  # Less than 1 KB
        size_str = f"{file_size} bytes"
    elif file_size < 1024 ** 2:  # Less than 1 MB
        size_str = f"{file_size / 1024:.2f} KB"
    else:  # Larger than 1 MB
        size_str = f"{file_size / (1024 ** 2):.2f} MB"

    # Print the file size
    print(f"Dataframe size: {len(aggregated_values)}")
    print(f"File size: {size_str}")

# Step 7: Display a message indicating the snapshots have been saved
print("Snapshots saved successfully.") 

# Add some prints yeah. But allow them to be turned off altogether. Perhaps seperate functions into stuff like the file size truncator.

