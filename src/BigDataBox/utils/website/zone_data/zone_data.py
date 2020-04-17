import csv
from json import dump

DIR_DATA = "../data/"

def zone_data():
	"""
		The API for all the zones in India

		This returns a JSON of all the districts with their corresponding value
	"""
	allData = {}

	with open('district_zones.csv', 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			stateBoi = row[0]
			districtBoi = row[1]
			value = int(row[2])
			if(districtBoi not in allData):
				allData[districtBoi] = {}
				allData[districtBoi]["state"] = stateBoi
				allData[districtBoi]["value"] = value

	with open(DIR_DATA + "APIData/zone_data.json", 'w') as FPtr:
		dump(allData, FPtr)