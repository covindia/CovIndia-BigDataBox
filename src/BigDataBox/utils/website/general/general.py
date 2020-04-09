"""
	This slave has one single source of running it's grunt work every single day:
	https://icecereal.github.io/img/blog-images/my-favorite-indie-band-uploaded-a-story-about-me/PrivatePresley-Keyboard.mp4

	Shamless Plug, yeh. Scru u. I wrote this, I get to plug whatever I want.

	It's a damn good cover too.

	Author: IceCereal.
"""

from datetime import datetime
from json import dump
from pandas import read_html
from bs4 import BeautifulSoup as bs
from requests import get

DIR_DATA = "../data/"

def general(data):
	"""
		The API function for general.

		Returns a JSON of general data including total infected, total dead, max infected and
		the rest you can see at the bottom where generalData is declared.

		Function returns DATA_general, to be used by general.district_values
	"""
	infectedTotal = 0
	deadTotal = 0
	DATA_general = {}

	for row in data:
		try:
			district = row[3]
		
		except:
			# No district
			district = ''

		# DIST_NA is a report in a state where the district is not known.
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

		# District already doesn't have an entry in DATA_general
		if district not in DATA_general:
			DATA_general[district] = {
				"infected" : 0,
				"dead" : 0,
				"state" : ""
			}

		try:
			DATA_general[district]["infected"] += int(row[4])
		except:
			# This only happens when row[4] is '' or ""
			pass

		try:
			DATA_general[district]["dead"] += int(row[5])
		except:
			# This only happens when row[5] is '' or ""
			pass

		# This isn't really required (or used anywhere) but we just keep assigning the state over & over again.
		# Possible TODO: assert that it doesn't change.
		try:
			DATA_general[district]["state"] = str(row[2])
		except:
			pass

	infectedMax = 0
	deadMax = 0

	districtsAffected = [] # List of districts with infected people
	statesAffected = [] # List of states with infected people

	# This loop primarily calculates our entries in generalData

	# Calculate the infectedMax and deadMax
	for district in DATA_general:
		# If district is DIST_NA, we skip. All the DIST_NA's across all rows would have piled up
		# in this (key, value) in DATA_general
		if district == "DIST_NA":
			continue

		# Simple check and resassign to get infectedMax
		if DATA_general[district]["infected"] > infectedMax:
			infectedMax = DATA_general[district]["infected"]

		# Simple check and resassign to get deadMax
		if DATA_general[district]["dead"] > deadMax:
			deadMax = DATA_general[district]["dead"]

		# districtsAffected is a list of all districts with infected people
		if district not in districtsAffected:
			districtsAffected.append(district)

		# statesAffected is a list of all states with infected people
		if DATA_general[district]["state"] not in statesAffected:
			statesAffected.append(DATA_general[district]["state"])

		# Calculating the total infected and dead
		infectedTotal += DATA_general[district]["infected"]
		deadTotal += DATA_general[district]["dead"]

	#### BELOW IS VERY VOLATILE CODE. HANDLE WITH CAUTION
	
	mohfwURL = "https://www.mohfw.gov.in/" # To get the total cured values

	r = get(mohfwURL)

	soup = bs(r.text, 'html.parser')

	lines = soup.prettify().split("\n")

	lineFlag = False

	# This isn't very pretty, but know that it works and their website is built like this.
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

	### VOLATILE CODE ENDS

	# Calculate the "value" of each district.
	# "value" corresponds to the color on the map

	# For now, value is calculated in a linear fashion.
	# However, an outlier (with a very high infected number) diminishes the value of other districts.
	# Hence, there are plans to convert this to a:
	# 	> logarithmic scale where the base is infectedMax to give a number between 0 & 1
	# 	> decible scale (logarithmic but multiplied)
	# 	> A vertically stretched sigmoid or arctan function
	#
	# Suggestions are welcome
	for district in DATA_general:
		DATA_general[district]["value"] = DATA_general[district]["infected"] / infectedMax

	# api.covindia.com/general
	generalData = {
		"deathTotal" : int(deadTotal),
		"districtList" : districtsAffected,
		"infectedTotal" : int(infectedTotal),
		"infectedMax" : int(infectedMax),
		"lastUpdatedTime" : str(datetime.now()),
		"statesList" : statesAffected,
		"totalCured" : int(TotalCured)
	}

	with open(DIR_DATA + "APIData/index_general.json", 'w') as FPtr:
		dump(generalData, FPtr)

	return DATA_general
