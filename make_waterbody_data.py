import json

#open two files that have information about waterbodies and their stations
waterbodies = open('colorado_waterbodies.tsv', 'r')
stations = open('colorado_stations.tsv', 'r')

wdict = {}
sdict = {}

#create a dictionary with information about the waterbody with waterbody name as the key
next(waterbodies)
for water in waterbodies:
	line = water.strip('\n')
	row = line.split('\t')
	geonames_url = row[0]
	name = row[1]
	drinking = row[3]
	cyan_id = row[4]
	recreation = row[16]
	wdict[name] = {'geonames':geonames_url, 'drinking':drinking, 'cyan_id': cyan_id, 'recreation':recreation}

#create a dictionary with information about the station, with waterbody name as the key
next(stations)
for station in stations:
	line = station.strip('\n')
	row = line.split('\t')
	waterbody = row[0]
	station = row[1]
	latitude = row[2]
	longitude = row[3]
	if waterbody in sdict:
		sdict[waterbody]['stations'].append([{'name':station, 'latitude':latitude, 'longitude':longitude}])
	else:
		sdict[waterbody] = {'stations':[{'name':station, 'latitude':latitude, 'longitude':longitude}]}

#merge the two dictionaries
keys = wdict.keys() | sdict.keys()

res = {k: {**wdict.get(k, {}), **sdict.get(k, {})} for k in keys}

#quality control - this should be 271
print(len(res))

#export merged dictionary as json file
with open("waterbody_station_data.json", "w") as outfile:
    json.dump(res, outfile)