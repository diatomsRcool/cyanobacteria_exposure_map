
in_file = open('CO-data-request-cyan_results.csv', 'r')
stations = open('colorado_stations.tsv', 'r')
out_file = open('CO_cyan_data.csv', 'w')
out_file.write('input_latitude,input_longitude,locationName,requestTimestamp,queryDate,imageDate,satelliteImageType,satelliteImageFrequency,cellConcentration_cells/mL,maxCellConcentration_cells/mL,cell_latitude,cell_longitude,validCellsCount,waterbody\n')

sta_dict = {}

next(stations)
for s in stations:
	s = s.strip('\n')
	w = s.split('\t')
	wb = w[0]
	station = w[1]
	latitude2 = w[2]
	longitude2 = w[3]
	latlon2 = str(latitude2) + str(longitude2)
	sta_dict[latlon2] = wb

next(in_file)
for f in in_file:
	f = f.strip('\n')
	r = f.split(',')
	latitude1 = r[0]
	longitude1 = r[1]
	latlon1 = str(latitude1) + str(longitude1)
	try:
		waterbody = sta_dict[latlon1]
		out_file.write(f + ',' + waterbody + '\n')
	except KeyError:
		print(f)
	
#8968
#8632