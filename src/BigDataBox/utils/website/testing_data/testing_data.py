"""
	Author: Srikar
"""

from json import dump
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

DIR_DATA = "../data/"
DIR_RES = "res/"

def testing_data(testing : bool = None):

	if(testing):
		return 1

	scope = ['https://spreadsheets.google.com/feeds']
	creds = ServiceAccountCredentials.from_json_keyfile_name(DIR_RES + 'creds.json',scope)
	client = gspread.authorize(creds)
	with open(DIR_RES + "URL_Testing", 'r') as F:
				URL = F.read()
	sheet = client.open_by_url(URL).worksheet('Sheet1')

	data = sheet.get()
	data = data[1:] # python is soo cool
	
	testingData = {}
	testingData["date"] = []
	testingData["tested"] = []
	testingData["positive"]= []
	testingData["percentage"] = []

	rowNum = 0

	for row in data:

		try:
			testingData["date"].append(row[0][:5]) #needed for making fronted's job easier, js is hard, python is cool(again)
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
	
	with open(DIR_DATA + "APIData/testing_data.json", 'w') as FPtr:
		dump(testingData, FPtr)