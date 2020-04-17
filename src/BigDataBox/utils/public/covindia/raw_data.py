"""
	This slave sure does have good taste in music.

	Listen to this: https://www.youtube.com/watch?v=XDpoBc8t6gE, is what it recommends. Lofi music
	is it's favorite genre.

	I agree.

	Author: LoFi-Head IceCereal
"""

from json import dump
from datetime import datetime
from collections import OrderedDict

DIR_DATA = "../data/"

def raw_data(data, testing : bool = None):
	"""
		The API function for raw-data. Saves output to DIR_DATA / PublicData / covindia_raw_data.json
	"""

	DATA_rd = OrderedDict()
	counter = 0

	# DATA_rd["reference"] = ["date", "time", "state", "district", "infected", "death", "source"]

	for row in data:
		localDict = OrderedDict()

		try:
			# DATE
			localDict["date"] = str(row[0])
		except:
			localDict["date"] = "NA"

		try:
			# TIME
			localDict["time"] = str(row[1])
		except:
			localDict["time"] = "NA"

		try:
			# DISTRICT
			localDict["district"] = str(row[3])
		except:
			localDict["district"] = "NA"

		try:
			# STATE
			localDict["state"] = str(row[2])
		except:
			localDict["state"] = "NA"

		try:
			# INFECTED
			localDict["infected"] = int(row[4])
		except:
			localDict["infected"] = 0

		try:
			# DEATH
			localDict["death"] = int(row[5])
		except:
			localDict["death"] = 0

		try:
			# SOURCE
			localDict["source"] = str(row[6])
		except:
			localDict["source"] = "NA"

		DATA_rd[counter] = localDict
		counter += 1

	if not testing:
		with open(DIR_DATA + "PublicData/covindia_raw_data.json", 'w') as FPtr:
			dump(DATA_rd, FPtr)

	return 1
