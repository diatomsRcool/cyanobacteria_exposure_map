import geopandas as gpd
import matplotlib.pyplot as plt

CO = gpd.read_file("/Volumes/PCCOMP/Colorado shape files/Colorado_State_Boundary/Colorado_State_Boundary.shp")
CO_zip = gpd.read_file("/Volumes/PCCOMP/Colorado shape files/Colorado_ZIP_Code_Tabulation_Areas_(ZCTA)/Colorado_ZIP_Code_Tabulation_Areas_(ZCTA).shp")
CO_water = gpd.read_file("/Volumes/PCCOMP/Colorado shape files/LAKES/LAKES.shp")
water = CO_water.to_crs(CO_zip.crs)

base = CO_zip.plot(color='white', edgecolor='black')
#base = CO.plot(color='white', edgecolor='black')

water.plot(ax=base)
#CO_zip.plot(ax=base)
plt.show()