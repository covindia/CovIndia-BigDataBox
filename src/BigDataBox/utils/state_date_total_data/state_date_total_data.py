"""
	https://www.youtube.com/watch?v=tc4ROCJYbm0 is all that drives this slave.

	Seeing a historical video drives this history buff to insansity sometimes. Ahh, it's a
	passionate little one, yes.

	The video is reallll good too.

	Author: IceCereal
"""

from datetime import datetime
from json import dump, load

DIR_DATA = "../data/"

def state_date_total_data(data):
	DATA_sdtd = {}
	states = []

	for row in data:
		try:
			DateUpdated = str(row[0])
		except:
			continue

		try:
			stateName = str(row[2])
		except:
			continue

		try:
			infected = int(row[4])
		except:
			infected = 0

		if DateUpdated not in DATA_sdtd:
			DATA_sdtd[DateUpdated] = {}
			for state in states:
				DATA_sdtd[DateUpdated][state] = 0
		if stateName not in states:
			states.append(stateName)
			for dateKey in DATA_sdtd:
				DATA_sdtd[dateKey][stateName] = 0
		DATA_sdtd[DateUpdated][stateName] += infected
		
	with open(DIR_DATA + "APIData/state_date_total_data.json", 'w') as FPtr:
		dump(DATA_sdtd, FPtr)

	return 1

