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
from math import log10

DIR_DATA = "../data/"

def decibel(X):
	"""
		Utility Function of a Utility Function to calculate:
			returns 10.0 * log (base 10) (X)
	"""
	if X == 0:
		return 0
	if X == 1:
		return 0.000001
	return (10.0 * log10 (X))

def inverse_decibel(X, split_number):
	"""
		The inverse of the decibel function. I.e., if you know the db value
		and you want to calculate the number that gives you the db value.

		args:
			X (float) : The Decibel
			split_number (float) : The number splits wanted in the legend

		returns:
			inv_dec (int) : The inverse_decibel value
	"""
	return int(10 ** (X / (10 * split_number)))

def general(data_new, data_cured, testing : bool = None):
	"""
		The API function for general.

		Returns a JSON of general data including total infected, total dead, max infected and
		the rest you can see at the bottom where generalData is declared.

		Function returns DATA_general, to be used by general.district_values
	"""

	deadMax = 0
	deadTotal = 0
	deadToday = 0
	infectedMax = 0
	infectedToday = 0
	infectedTotal = 0

	dateToday = datetime.today().date()

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

		# This cannot be in a try ... except. We need to know if anything was entered wrong.
		DateUpdated = datetime.strptime(DateUpdated, "%d/%m/%Y").date()

		# Today's Statistics
		if DateUpdated == dateToday:
			try:
				deadToday += int(row[5])
			except:
				pass
			try:
				infectedToday += int(row[4])
			except:
				pass

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

		# Calculating the total infected and dead
		infectedTotal += DATA_general[district]["infected"]
		deadTotal += DATA_general[district]["dead"]

	# Cured Data
	totalCured = 0
	for row in data_cured:
		try:
			totalCured += int(row[4])
		except:
			totalCured += 0

	# Calculate the "value" of each district.
	# "value" corresponds to the color on the map

	# For now, value is calculated as decibels.
	#
	# It was previously linear which had the problem with an outlier (with a very high infected number).
	# It diminished the value of other districts.

	# Step 1. Calculate the raw decibels and keep track of the highest

	highestValue = 0

	for district in DATA_general:
		districtValue = decibel(DATA_general[district]["infected"])

		if districtValue > highestValue:
			highestValue = districtValue

		DATA_general[district]["value"] = districtValue

	# Step 2. Make all the values divided by highestValue [To get numbers between 0 & 1]
	for district in DATA_general:
		DATA_general[district]["value"] = DATA_general[district]["value"] / highestValue

	# Step 3. Calculate the 2 points that correspond to highestValue/3 and 2*highestValue/3
	#
	# If 10 log10 (X1) = highestValue/3
	# Then X1 = 10 ^ (highestValue/30)
	#
	# If 10 log10 (X2) = 2*highestValue/3
	# Then X2 = 10 ^ (2*highestValue/30)

	X1 = inverse_decibel(1 * highestValue, 3)
	X2 = inverse_decibel(2 * highestValue, 3)

	# api.covindia.com/general
	generalData = {
		"deadToday" : int(deadToday),
		"deathTotal" : int(deadTotal),
		"infectedTotal" : int(infectedTotal),
		"infectedMax" : int(infectedMax),
		"infectedToday" : int(infectedToday),
		"lastUpdatedTime" : str(datetime.now()),
		"splitPoints" : [1, X1, X2, int(infectedMax)],
		"totalCured" : int(totalCured)
	}

	if not testing:
		with open(DIR_DATA + "APIData/index_general.json", 'w') as FPtr:
			dump(generalData, FPtr)

	return DATA_general
