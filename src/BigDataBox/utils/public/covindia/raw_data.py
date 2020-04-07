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

def raw_data(data):
	"""
		The API function for raw-data. Saves output to DIR_DATA / PublicData / covindia_raw_data.json
	"""

	DATA_rd = OrderedDict()
	counter = 0

	DATA_rd["reference"] = ["date", "time", "state", "district", "infected", "death", "source"]

	for row in data:
		localList = []

		try:
			# DATE
			localList.append(str(row[0]))
		except:
			localList.append("NA")

		try:
			# TIME
			localList.append(str(row[1]))
		except:
			localList.append("NA")

		try:
			# STATE
			localList.append(str(row[2]))
		except:
			localList.append("NA")

		try:
			# DISTRICT
			localList.append(str(row[3]))
		except:
			localList.append("NA")

		try:
			# INFECTED
			localList.append(int(row[4]))
		except:
			localList.append(0)

		try:
			# DEATH
			localList.append(int(row[5]))
		except:
			localList.append(0)

		try:
			# SOURCE
			localList.append(str(row[6]))
		except:
			localList.append("NA")

		DATA_rd[counter] = localList
		counter += 1

	with open(DIR_DATA + "PublicData/covindia_raw_data.json", 'w') as FPtr:
		dump(DATA_rd, FPtr)

	return 1