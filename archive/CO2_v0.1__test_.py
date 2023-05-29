# Only plot microsim vehicles moving without indicators
import geopandas as gpd
import pandas as pd
# import geoplot as gplt
import time
import matplotlib.pyplot as plt
import contextily as cx
import os
from shapely import wkt, geometry
import numpy as np
import sys

# from functools import partial


plt.ioff()
plt.switch_backend('agg') # to export plots as images

# suffix = '2_16'
# if no error pops up, remove #

# receivers_path = r"C:\Users\Sacha\Documents\KTH\Data\Tartu\receivers_python_method1_5m_pop.shp"
buildings_path = r"C:\Users\Pro\OneDrive - CentraleSupelec\Bureau\KTH\pollutant_emissions\example_sodermalm\buildings_sodermalm.shp"
roads_path = r"C:\Users\Pro\OneDrive - CentraleSupelec\Bureau\KTH\pollutant_emissions\example_sodermalm\roads_cleaned_sodermalm.shp"
# lday_path = r"C:\Users\Sacha\Documents\KTH\Data\Tartu\statistical_paper\tests\fcd_output\results\levels_per_receivers_" + suffix + ".csv"

microsim_path = r"C:\Users\Pro\OneDrive - CentraleSupelec\Bureau\KTH\pollutant_emissions\example_sodermalm\fcdgeo5minCSV.csv"
# microsim_light_path = r"C:\Users\Sacha\Documents\KTH\Data\Tartu\Tartu 24h traffic sim\1 hour micro sim test 2\fcd_output\fcd_output_light.csv"

output_dir = r"C:\Users\Pro\OneDrive - CentraleSupelec\Bureau\KTH\pollutant_emissions\output"

# proj = '32635'

t_min = 20001
t_max = 20300

print("Loading files...")
# receivers = gpd.read_file(receivers_path).to_crs(epsg=3857)
buildings = gpd.read_file(buildings_path).to_crs(epsg=3857)
# EPSG 3857 CRS is pseudo Mercator
roads = gpd.read_file(roads_path).to_crs(epsg=3857)
# lday = pd.read_csv(lday_path, engine="pyarrow")
# lday_merged = lday.merge(receivers, left_on="IDRECEIVER", right_on="pk", suffixes=("_ld", None))
# lday_merged = lday_merged[['timestep', 'IDRECEIVER', 'LAEQ', 'pop', 'geometry']]
# lday_merged = gpd.GeoDataFrame(lday_merged, crs="EPSG:3857", geometry="geometry")

print("Loading traffic...")

# if loading from CSV:
traffic_data = pd.read_csv(microsim_path, usecols=['x', 'y', 'timestep', 'CO2'], engine="pyarrow")
traffic_data = traffic_data[(traffic_data['timestep']>=t_min) & (traffic_data['timestep']<t_max)]
# co2_aggregated = traffic_data.groupby(['x', 'y'])['CO2'].sum()

print('- Loading coordinates...')
traffic_data = gpd.GeoDataFrame(traffic_data,
								geometry=gpd.points_from_xy(traffic_data["x"], traffic_data["y"]),
								crs="EPSG:4326")
print("- Reprojecting...")
traffic_data = traffic_data[['timestep', 'CO2', 'geometry']].to_crs(epsg=3857)


# # if loading from a shapefile:
# traffic_data = gpd.read_file(microsim_path) #.shp file
# print("- Reprojecting...")
# traffic_data = traffic_data[['timestep', 'geometry']].to_crs(epsg=3857)


# boundaries of the area of interest:
min_x, min_y, max_x, max_y = traffic_data.geometry.total_bounds
cumulative_co2 = np.zeros_like(traffic_data[traffic_data['timestep'] == t_min])

print("Filtering...")
for t in range(t_min, t_max):
	print(t)
	traffic_filtered = traffic_data[traffic_data['timestep'] == t]

	# plot microscopic traffic vehicles:
	ax = traffic_filtered.plot(
		markersize=5,
		column="CO2",
		cmap="viridis",
		marker='o',
		edgecolors="blue"
	)

	# lday_filtered.plot(
	# 	ax = ax,
	# 	column='LAEQ', 
	# 	cmap='magma', 
	# 	markersize=4, 
	# 	figsize=(10, 10), 
	# 	legend=(t==t_min), 
	# 	vmin=0,
	# 	vmax=70
	# 	)

	# add background image from OpenStreetMap:
	cx.add_basemap(
		ax, 
		crs=traffic_filtered.crs.to_string(), 
		source=cx.providers.OpenStreetMap.Mapnik, 
		zoom=13, 
		alpha=0.5
		)


	ax.set_xlim([min_x, max_x])
	ax.set_ylim([min_y, max_y])
	plt.axis('off')
	plt.savefig(os.path.join(output_dir, 'abs_lvls_' + str(t) + '.jpg'), dpi=250, bbox_inches='tight')
	plt.close()

	Could
	you
	wrap
	this
	up in one, continuous
	Python
	script, where
	each
	section is commented
	with detailed yet concise explanation of what's going on?