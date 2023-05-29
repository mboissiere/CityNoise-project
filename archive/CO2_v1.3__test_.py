import os
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

# Specify the CRS
crs = 'EPSG:3857'

# Read the CSV data
data = gpd.read_csv('traffic_data.csv', usecols=['timestep', 'longitude', 'latitude', 'CO2'], dtype={'timestep': int, 'longitude': float, 'latitude': float, 'CO2': float})

# Create the GeoDataFrame
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['longitude'], data['latitude']))

# Set the CRS for the GeoDataFrame
gdf.crs = crs

# Define the version number
version = 'v3'

# Create output folder for the version
output_folder = f'output_{version}'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Project the CSV data to the chosen CRS
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['longitude'], data['latitude']))
gdf = gdf.set_crs(crs)

# Group data by latitude and longitude, and calculate the sum of CO2 values for each location
grouped = gdf.groupby(['latitude', 'longitude'])['CO2'].sum()

# Calculate the maximum CO2 pollution at a single point
max_pollution = grouped.max()

# Determine the appropriate unit for the colorbar
if max_pollution >= 1000:
    gdf['CO2'] = gdf['CO2'] / 1000
    unit = 'kilograms'
    if max_pollution >= 1000:
        gdf['CO2'] = gdf['CO2'] / 1000
        unit = 'tons'
else:
    unit = 'grams'

# Create the plot
fig, ax = plt.subplots(figsize=(10, 10))

# Set the extent based on the projected data
minx, miny, maxx, maxy = gdf.geometry.total_bounds
ax.set_xlim(minx, maxx)
ax.set_ylim(miny, maxy)

# Add the OpenStreetMap basemap
ctx.add_basemap(ax, crs=crs, source=ctx.providers.OpenStreetMap.Mapnik)

# Plot the CO2 data
sc = ax.scatter(gdf.geometry.x, gdf.geometry.y, c=gdf['CO2'], s=5, cmap='viridis')

# Add colorbar
cbar = plt.colorbar(sc, ax=ax, fraction=0.03, pad=0.04)
cbar.set_label('CO2 pollution ({})'.format(unit))

# Set labels and title
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('CO2 Pollution')

# Save the snapshot to the output folder
output_file = os.path.join(output_folder, f'snapshot_{version}.png')
plt.savefig(output_file)

# Show the plot
plt.show()
