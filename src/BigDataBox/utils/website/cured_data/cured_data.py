"""
	Author: Srikar
"""

from json import dump
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

DIR_DATA = "../data/"
DIR_RES = "res/"

def isToday(date): #TooLazytoTypeStuff
	return (date == datetime.now().strftime("%d/%m/%Y"))

def cured_data(testing : bool = None):

	if(testing):
		return 1

	scope = ['https://spreadsheets.google.com/feeds']
	creds = ServiceAccountCredentials.from_json_keyfile_name(DIR_RES + 'creds.json',scope)
	client = gspread.authorize(creds)
	with open(DIR_RES + "URL_Cured", 'r') as F:
				URL = F.read()
	sheet = client.open_by_url(URL).worksheet('Sheet1')

	data = sheet.get()
	data = data[1:] # python is soo cool again
	
	cured_data = {}

	for row in data:

		date = row[0]
		state = row[2]

		if(state in cured_data):
			
			try:
				cured_data[state]["testedTotal"] += int(row[3])
			except:
				pass

			try:
				cured_data[state]["curedTotal"] += int(row[4])
			except:
				pass

			if(isToday(date)):

				try:
					cured_data[state]["testedToday"] += int(row[3])
				except:
					pass

				try:
					cured_data[state]["curedToday"] += int(row[4])
				except:
					pass
			
		else:

			cured_data[state] = {}

			cured_data[state]["testedTotal"] = 0
			cured_data[state]["curedTotal"] = 0
			cured_data[state]["testedToday"] = 0
			cured_data[state]["curedToday"] = 0

			try:
				cured_data[state]["testedTotal"] += int(row[3])
			except:
				pass

			try:
				cured_data[state]["curedTotal"] += int(row[4])
			except:
				pass

			if(isToday(date)):

				try:
					cured_data[state]["testedToday"] += int(row[3])
				except:
					pass

				try:
					cured_data[state]["curedToday"] += int(row[4])
				except:
					pass


	with open(DIR_DATA + "APIData/cured_data.json", 'w') as FPtr:
		dump(cured_data, FPtr)