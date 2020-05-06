"""
	Author: Srikar
"""

from json import dump
from datetime import datetime

DIR_DATA = "../data/"
DIR_RES = "res/"

def testing(data_testing, testing : bool = None):
	testingData = {}
	testingData["date"] = []
	testingData["tested"] = []
	testingData["positive"]= []
	testingData["percentage"] = []

	rowNum = 0

	for row in data_testing:

		try:
			testingData["date"].append(row[0][:5]) #needed for making frontend's job easier, js is hard, python is cool(again)
		except:
			testingData["date"].append("NA")

		try:
			testingData["tested"].append(int(row[3]))
		except:
			testingData["tested"].append("NA")
		
		try:
			testingData["positive"].append(int(row[5]))
		except:
			testingData["positive"].append("NA")

		try: #without = round, we'll end up having 10 decimal places, nobody wants that.
			testingData["percentage"].append(round((testingData["positive"][rowNum]/testingData["tested"][rowNum]) * 100, 3))
		except:
			testingData["percentage"].append("NA")
		
		rowNum += 1
	
	if not testing:
		with open(DIR_DATA + "APIData/history_testing.json", 'w') as FPtr:
			dump(testingData, FPtr)

	return 1