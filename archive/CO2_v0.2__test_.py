import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from matplotlib.animation import FuncAnimation

# Step 1: Read the CSV file into a Pandas DataFrame, handling missing values
data = pd.read_csv('traffic_data.csv', usecols=['timestep', 'longitude', 'latitude', 'CO2'], dtype={'timestep': 'Int64', 'longitude': float, 'latitude': float, 'CO2': float}, na_values='')

# Step 2: Create a GeoDataFrame from the DataFrame
crs = 'EPSG:4326'  # Assuming latitude and longitude are in WGS84
geometry = gpd.points_from_xy(data['longitude'], data['latitude'])
gdf = gpd.GeoDataFrame(data, geometry=geometry, crs=crs)

# Step 3: Calculate the bounding box coordinates
min_lon, min_lat, max_lon, max_lat = gdf.total_bounds

# Step 4: Set up the figure and axes
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_aspect('equal')
ax.set_axis_off()

# Step 5: Plot the background map
ctx.add_basemap(ax, crs=crs, source=ctx.providers.OpenStreetMap.Mapnik, alpha=0.5)
ax.set_xlim(min_lon, max_lon)
ax.set_ylim(min_lat, max_lat)

# Step 6: Define the update function for animation
def update(frame):
    ax.clear()
    ax.set_aspect('equal')
    ax.set_axis_off()
    ctx.add_basemap(ax, crs=crs, source=ctx.providers.OpenStreetMap.Mapnik, alpha=0.5)
    timestep_data = gdf[gdf['timestep'] == frame]
    sc = ax.scatter(
        timestep_data.geometry.x,
        timestep_data.geometry.y,
        c=timestep_data['CO2'],
        cmap='coolwarm',
        s=5,
        vmin=data['CO2'].min(),
        vmax=data['CO2'].max(),
    )
    ax.set_xlim(min_lon, max_lon)
    ax.set_ylim(min_lat, max_lat)
    return sc

# Step 7: Create the animation
animation = FuncAnimation(fig, update, frames=data['timestep'].unique(), interval=200)

# Step 8: Create the colorbar after the initial frame has been rendered
sc = update(data['timestep'].unique()[0])  # Get the scatter plot object from the first frame
cbar = fig.colorbar(sc, ax=ax, label='CO2 Pollution')

# Step 9: Show the animation
plt.show()
