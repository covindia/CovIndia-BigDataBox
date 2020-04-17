"""
	Author: Srikar
"""

import csv
from json import dump

DIR_DATA = "../data/"

def zone_data():
	"""
		The API for all the zones in India

		This returns a JSON of all the districts with their corresponding value
	"""
	allData = {}

	# State, District Name, Value
	# row[0], row[1],	row[2]
	with open('res/district_zones.csv', 'r') as file:
		reader = csv.reader(file)
		rowCount = False
		for row in reader:
			if(not rowCount):
				rowCount = not rowCount
				continue
			state = row[0]
			district = row[1]
			value = int(row[2])
			if(district not in allData):
				allData[district] = {}
				allData[district]["state"] = state
				allData[district]["value"] = value
	
	with open(DIR_DATA + "APIData/zone_data.json", 'w') as FPtr:
		dump(allData, FPtr)

	return 1