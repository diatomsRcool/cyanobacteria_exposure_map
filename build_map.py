import geopandas as gpd
import matplotlib.pyplot as plt

CO = gpd.read_file("/Volumes/PCCOMP/Colorado shape files/Colorado_State_Boundary/Colorado_State_Boundary.shp")

CO.plot()
plt.show()