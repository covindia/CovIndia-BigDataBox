"""
	Author: Srikar
"""

from json import dump
from datetime import datetime

DIR_DATA = "../data/"
DIR_RES = "res/"

def isToday(date): #TooLazytoTypeStuff
	return (date == datetime.now().strftime("%d/%m/%Y"))

def cured_tested_values(data_cured, testing : bool = None):	
	DATA_cured = {}

	for row in data_cured:

		date = row[0]
		state = row[2]

		if(state in DATA_cured):
			
			try:
				DATA_cured[state]["testedTotal"] += int(row[3])
			except:
				pass

			try:
				DATA_cured[state]["curedTotal"] += int(row[4])
			except:
				pass

			if(isToday(date)):

				try:
					DATA_cured[state]["testedToday"] += int(row[3])
				except:
					pass

				try:
					DATA_cured[state]["curedToday"] += int(row[4])
				except:
					pass
			
		else:

			DATA_cured[state] = {}

			DATA_cured[state]["testedTotal"] = 0
			DATA_cured[state]["curedTotal"] = 0
			DATA_cured[state]["testedToday"] = 0
			DATA_cured[state]["curedToday"] = 0

			try:
				DATA_cured[state]["testedTotal"] += int(row[3])
			except:
				pass

			try:
				DATA_cured[state]["curedTotal"] += int(row[4])
			except:
				pass

			if(isToday(date)):

				try:
					DATA_cured[state]["testedToday"] += int(row[3])
				except:
					pass

				try:
					DATA_cured[state]["curedToday"] += int(row[4])
				except:
					pass

	with open(DIR_DATA + "APIData/present_cured_tested_values.json", 'w') as FPtr:
		dump(DATA_cured, FPtr)