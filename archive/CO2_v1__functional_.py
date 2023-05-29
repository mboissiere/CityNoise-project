import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx

# Create the "output" folder if it doesn't exist
if not os.path.exists('output'):
    os.makedirs('output')

# Step 1: Read the CSV file into a Pandas DataFrame, filtering out rows with N/A timesteps
data = pd.read_csv('traffic_data.csv', usecols=['timestep', 'longitude', 'latitude', 'CO2'],
                   dtype={'timestep': float, 'longitude': float, 'latitude': float, 'CO2': float}).dropna(
    subset=['timestep'])

# Convert the "timestep" column to integer type
data['timestep'] = data['timestep'].astype(int)

# Step 2: Create a GeoDataFrame from the DataFrame
geometry = gpd.points_from_xy(data['longitude'], data['latitude'])
gdf = gpd.GeoDataFrame(data, geometry=geometry)

# Step 3: Calculate the bounding box coordinates
min_lon, min_lat, max_lon, max_lat = gdf.total_bounds

# Step 4: Calculate the maximum CO2 value for the colorbar range
max_CO2 = data['CO2'].sum()  # Summing CO2 over all timesteps

# Specify the desired zoom level for the basemap
zoom_level = 18

# Step 5: Set up the figure and axes
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_aspect('equal')
ax.set_axis_off()

# Add the basemap with the specified zoom level
ctx.add_basemap(ax, crs=gdf.crs, source=ctx.providers.OpenStreetMap.Mapnik, alpha=0.5, zoom=zoom_level)

# Initialize the colorbar with the maximum CO2 value
sc = ax.scatter([], [], c=[], cmap='coolwarm', s=5, vmin=0, vmax=max_CO2)
cbar = plt.colorbar(sc, ax=ax, label='CO2 Pollution (grams)', shrink=0.6)

# Step 6: Loop over each timestep and update the CO2 values
aggregated_data = gdf.groupby(['longitude', 'latitude'])['CO2'].cumsum()

# Loop over each timestep and update the scatter plot
for timestep in data['timestep'].unique():
    ax.clear()
    ax.set_aspect('equal')
    ax.set_axis_off()
    ctx.add_basemap(ax, crs=gdf.crs, source=None, zoom=zoom_level)

    # Filter data for the current timestep and aggregate CO2 values
    timestep_data = gdf[gdf['timestep'] <= timestep]
    aggregated_values = aggregated_data[timestep_data.index]

    sc = ax.scatter(
        timestep_data.geometry.x,
        timestep_data.geometry.y,
        c=aggregated_values,
        cmap='coolwarm',
        s=5,
        vmin=0,
        vmax=max_CO2,
    )
    ax.set_xlim(min_lon, max_lon)
    ax.set_ylim(min_lat, max_lat)

    plt.savefig(f'output/snapshot_{timestep}.png', dpi=300, bbox_inches='tight')

# Step 7: Display a message indicating the snapshots have been saved
print("Snapshots saved successfully.")
