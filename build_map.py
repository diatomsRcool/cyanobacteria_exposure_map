import geopandas as gpd
import matplotlib.pyplot as plt

#loading three shape files
CO = gpd.read_file("/Volumes/PCCOMP/Colorado shape files/Colorado_State_Boundary/Colorado_State_Boundary.shp")
CO_zip = gpd.read_file("/Volumes/PCCOMP/Colorado shape files/Colorado_ZIP_Code_Tabulation_Areas_(ZCTA)/Colorado_ZIP_Code_Tabulation_Areas_(ZCTA).shp")
CO_water = gpd.read_file("/Volumes/PCCOMP/Colorado shape files/LAKES/LAKES.shp")

#Transform water shape file so that it uses the same coordinate reference system as the zip code shape file
water = CO_water.to_crs(CO_zip.crs)

#set the zip code map as the base map
base = CO_zip.plot(color='white', edgecolor='black')

#plot the water on top of the zip codes and show
water.plot(ax=base)
plt.show()