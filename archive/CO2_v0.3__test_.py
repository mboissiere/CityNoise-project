import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx

# Create the "output" folder if it doesn't exist
if not os.path.exists('output'):
    os.makedirs('output')

# Step 1: Read the CSV file into a Pandas DataFrame
data = pd.read_csv('traffic_data.csv', usecols=['timestep', 'longitude', 'latitude', 'CO2'], dtype={'timestep': int, 'longitude': float, 'latitude': float, 'CO2': float})

# Step 2: Create a GeoDataFrame from the DataFrame
geometry = gpd.points_from_xy(data['longitude'], data['latitude'])
gdf = gpd.GeoDataFrame(data, geometry=geometry)

# Step 3: Calculate the bounding box coordinates
min_lon, min_lat, max_lon, max_lat = gdf.total_bounds

# Step 4: Calculate the maximum CO2 value for the colorbar range
max_CO2 = data['CO2'].sum()  # Summing CO2 over all timesteps

# Step 5: Set up the figure and axes
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_aspect('equal')
ax.set_axis_off()

# Add the basemap
ctx.add_basemap(ax, crs=gdf.crs, source=ctx.providers.OpenStreetMap.Mapnik, alpha=0.5)

# Initialize the colorbar with the maximum CO2 value
sc = ax.scatter([], [], c=[], cmap='coolwarm', s=5, vmin=0, vmax=max_CO2)
cbar = plt.colorbar(sc, ax=ax, label='CO2 Pollution (grams)', shrink=0.6)

# Step 6: Loop over each timestep and update the scatter plot
for timestep in data['timestep'].unique():
    ax.clear()
    ax.set_aspect('equal')
    ax.set_axis_off()
    ctx.add_basemap(ax, crs=gdf.crs, source=None)
    timestep_data = gdf[gdf['timestep'] == timestep]
    sc = ax.scatter(
        timestep_data.geometry.x,
        timestep_data.geometry.y,
        c=timestep_data['CO2'],
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
