"""
	Man, who let the onion ninja's in?

	https://www.youtube.com/watch?v=lq8QVqh14Wc is this weeb slave's favorite video.

	Full Metal Alchemist: Brotherhood is definitely this slave's favorite Anime, so much so that
	it named it's computer after Winry, the beautiful beautiful waifu.

	Gotta say, hard to argue with this slave of culture.

	Author: Renkinjustu-shi IceCereal
"""

from json import dump
from datetime import datetime
from collections import OrderedDict
from pandas import read_html
from bs4 import BeautifulSoup as bs
from requests import get

DIR_DATA = "../data/"

def general_data(data, testing : bool = True):
	"""
		The API function for general data. Saves output to DIR_DATA / PublicData / covindia_general_data.json
	"""
	infectedTotal = 0
	deadTotal = 0
	globalData = {}
	returnData = {}

	for row in data:
		try:
			district = row[3]
		except:
			pass

		if district == "DIST_NA":
			try:
				infectedTotal += int(row[4])
			except:
				pass
			try:
				deadTotal += int(row[5])
			except:
				pass

		try:
			TimeUpdated = str(row[1])
		except:
			TimeUpdated = "00:00"
		try:
			DateUpdated = str(row[0])
		except:
			DateUpdated = datetime.now().strftime("%d/%m/%Y")

		returnDict = {}

		if district in globalData:
			try:
				globalData[district]["infected"] += int(row[4])
				returnDict["infected"] = int(row[4])
			except:
				returnDict["infected"] = 0

			try:
				globalData[district]["dead"] += int(row[5])
				returnDict["dead"] = int(row[5])
			except:
				returnDict["dead"] = 0

			try:
				returnDict["state"] = str(row[2])
			except:
				returnDict["state"] = ""

			try:
				returnDict["source"] = str(row[6])
			except:
				returnDict["source"] = ""


		else:
			globalData[district] = {}
			try:
				globalData[district]["infected"] = int(row[4])
				returnDict["infected"] = int(row[4])
			except:
				globalData[district]["infected"] = 0
				returnDict["infected"] = 0

			try:
				globalData[district]["dead"] = int(row[5])
				returnDict["dead"] = int(row[5])
			except:
				globalData[district]["dead"] = 0
				returnDict["dead"] = 0
			try:
				globalData[district]["state"] = str(row[2])
				returnDict["state"] = str(row[2])
			except:
				globalData[district]["state"] = ""
				returnDict["state"] = ""

			try:
				globalData[district]["source"] = str(row[6])
				returnDict["source"] = str(row[6])
			except:
				globalData[district]["source"] = ""
				returnDict["source"] = ""

		DateTime = DateUpdated +" "+ TimeUpdated
		returnDict["time"] = DateTime

		if district in returnData:
			returnData[district].append(returnDict)
		else:
			returnData[district] = [returnDict]

	infectedMax = 0
	deadMax = 0

	districtsAffected = []
	statesAffected = []

	for district in globalData:
		if district == "DIST_NA":
			continue
		if globalData[district]["infected"] > infectedMax:
			infectedMax = globalData[district]["infected"]
		if globalData[district]["dead"] > deadMax:
			deadMax = globalData[district]["dead"]

		if district not in districtsAffected:
			districtsAffected.append(district)

		if globalData[district]["state"] not in statesAffected:
			statesAffected.append(globalData[district]["state"])

		infectedTotal += globalData[district]["infected"]
		deadTotal += globalData[district]["dead"]

	mohfwURL = "https://www.mohfw.gov.in/"

	r = get(mohfwURL)

	soup = bs(r.text, 'html.parser')

	lines = soup.prettify().split("\n")

	lineFlag = False

	for lineNumber in range(len(lines)):
		if "icon-inactive.png" in lines[lineNumber]:
			if "strong" in lines[lineNumber+1]:
				if "Cured" in lines[lineNumber+5]:
					lineFlag = True
					lineTarget = lines[lineNumber+2]
					break

	if not lineFlag:
		raise NameError("cured number in MOHFW wasn't found. :|")

	lineTarget = lineTarget.replace(" ", "")
	lineTarget = lineTarget.replace("\t", "")

	TotalCured = int(lineTarget)

	generalData = {
		"deathTotal" : int(deadTotal),
		"districtList" : districtsAffected,
		"infectedTotal" : int(infectedTotal),
		"infectedMax" : int(infectedMax),
		"lastUpdatedTime" : str(datetime.now()),
		"statesList" : statesAffected,
		"totalCured" : int(TotalCured)
	}

	if not testing:
		with open(DIR_DATA + "PublicData/covindia_general_data.json", 'w') as FPtr:
			dump(generalData, FPtr)

	return 1
