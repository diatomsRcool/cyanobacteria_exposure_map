import pandas as pd

sat_obs = pd.read_csv('CO-data-request-cyan_results.csv', index_col=False, usecols=['input_latitude','input_longitude','locationName','imageDate','cellConcentration_cells/mL','maxCellConcentration_cells/mL','cell_latitude','cell_longitude','validCellsCount'])
sat_obs['imageDate']=pd.to_datetime(sat_obs['imageDate'], format='%m-%d-%Y %H:%M:%S:%f UTC', errors='coerce')
sat_obs['year'] = sat_obs['imageDate'].dt.year
sat_obs['latlon'] = sat_obs['input_latitude'].astype(str) + sat_obs['input_latitude'].astype(str)
#print(sat_obs)
cell_conc_summary = sat_obs.groupby(['input_latitude','input_longitude','locationName']).aggregate({'maxCellConcentration_cells/mL':'max', 'cellConcentration_cells/mL':'min', 'year':'nunique', 'latlon':'count'})
print(cell_conc_summary)
#sat_obs_summary = cell_conc_summary.merge(sat_obs, how='left', on=['input_latitude','input_longitude'])
#print(sat_obs_summary)
"""
in_file.open=('CO-data-request-cyan_results.csv', 'r')

out_file.open=('sat_obs_summary.txt', 'a')

for line in in_file:
	line = line.strip()
	row = line.split(',')
	latitude = row[0]
	longitude = row[1]
	name = row[2]
	date = row[5]
	mincell = row[8]
	maxcell = row[9]
"""
