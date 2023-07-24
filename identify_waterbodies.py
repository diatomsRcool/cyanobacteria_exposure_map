import pandas as pd
import json

# Opening JSON file
f = open('waterbody_station_data.json')
  
waterbody_data = json.load(f)

sat_obs = pd.read_csv('CO_cyan_data.csv', index_col=False, usecols=['input_latitude','input_longitude','locationName','imageDate','cellConcentration_cells/mL','maxCellConcentration_cells/mL','cell_latitude','cell_longitude','validCellsCount','waterbody'])
sat_obs['imageDate']=pd.to_datetime(sat_obs['imageDate'], format='%m-%d-%Y %H:%M:%S:%f UTC', errors='coerce')
sat_obs['year'] = sat_obs['imageDate'].dt.year
sat_obs['month'] = sat_obs['imageDate'].dt.month

#latlon can be a proxy for station
sat_obs['latlon'] = sat_obs['input_latitude'].astype(str) + sat_obs['input_latitude'].astype(str)

#this line creates the waterbody summary dataframe that we can use to identify waterbodies of interest
cell_conc_summary = sat_obs.groupby(['waterbody']).aggregate({'maxCellConcentration_cells/mL':'max', 'cellConcentration_cells/mL':'min', 'year':'nunique', 'waterbody':'count'})
cell_conc_summary = cell_conc_summary.rename(columns={'waterbody':'no. obs'})

#this code creates a dataframe of waterbodies that are likely to have chronic, toxin-producing cyanobacteria blooms
for index, row in cell_conc_summary.iterrows():
	if row['year'] >= 3 and row['maxCellConcentration_cells/mL'] > 999999:
		try:
			if waterbody_data[index]['toxins_tested'] == 'Y' and waterbody_data[index]['toxins confirmed'] == 'N':
				continue
			else:
				cell_conc_summary.loc[index, 'exposure'] = 'chronic'
		except KeyError:
			print(waterbody_data[index])
chronic = cell_conc_summary.loc[cell_conc_summary['exposure'] == 'chronic']
for index, row in chronic.iterrows():
	chronic.loc[index, 'centroid_lat'] = waterbody_data[index]['centroid_lat']
	chronic.loc[index, 'centroid_lon'] = waterbody_data[index]['centroid_lon']
chronic = chronic.rename(columns={'maxCellConcentration_cells/mL':'max cells/mL'})
chronic = chronic.rename(columns={'cellConcentration_cells/mL':'min cells/mL'})
chronic = chronic.rename(columns={'year':'no. years'})
print(len(chronic))
chronic.to_csv('potential_chronic.csv')

"""
#This code can tell you how many observations occur by month
m = sat_obs.groupby(['month']).count()
print(m)
#there are observations in every month
#most observations occur in July, August, Sept, Oct (order of magnitude higher)
#need to get the prevailing winds for these months only? or all months?

#these are the waterbodies that only have observations in Jan or Feb. May need to remove these.
They might have false positives in the satellite data. Need to confirm with local authorities.
Spot check showed no local confirmation data
{'Ralston Reservoir', 'Eastdale Reservoir Number 1', 'Beckwith Reservoir', 'Windsor Reservoir Number 8', 'Unnamed Waterbody No. 3', 'Pueblo Reservoir', 'Hertha Reservoir', 'Cobb Lake', 'Hallenbeck Reservoir', 'Cooley Lake', 'Aurora-Rampart Reservoir', 'Boyd Lake', 'Dixon Reservoir', 'Lindenmeier Lake', 'College Lake', 'Unnamed Waterbody No. 7', 'Lon Hagler Reservoir'}

#This block of code looks at waterbodies that only have CyAN observations in Jan or Feb.
#Winter is an unusual time for cyanobacteria. I am concerned these are false positives.
winter_lake = []
summer_lake = []
for index, row in sat_obs.iterrows():
	if row['month'] == 1 or row['month'] == 2:
		winter_lake.append(row['waterbody'])
	elif row['month'] == 7 or row['month'] == 8 or row['month'] == 9 or row['month'] == 10:
		summer_lake.append(row['waterbody'])
print('winter lake')
winter_lake = set(winter_lake)
print(len(winter_lake))
print('summer lake')
summer_lake = set(summer_lake)
print(len(summer_lake))
print('summer observations and no winter observations')
print(summer_lake - winter_lake)
print(len(summer_lake - winter_lake))
print('winter observations and no summer observations')
m = winter_lake - summer_lake
print(m)
print(len(m))
"""
