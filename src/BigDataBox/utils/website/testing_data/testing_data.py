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

	rowNum = 0

	for row in data:
		testingData[rowNum] = {}
		testingData[rowNum]["date"] = row[0]

		#testingData[rowNum]["time"] = row[1]

		try:
			testingData[rowNum]["tested"] = int(row[3])
		except:
			testingData[rowNum]["tested"] = "NA"
		
		try:
			testingData[rowNum]["positive"] = int(row[5])
		except:
			testingData[rowNum]["positive"] = "NA"

		try:
			testingData[rowNum]["percentage"] = round((testingData[rowNum]["positive"]/testingData[rowNum]["tested"]) * 100, 3)
		except:
			testingData[rowNum]["percentage"] = "NA"
		
		rowNum += 1
	
	with open(DIR_DATA + "APIData/testing_data.json", 'w') as FPtr:
		dump(testingData, FPtr)