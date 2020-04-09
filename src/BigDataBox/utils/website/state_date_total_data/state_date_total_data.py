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
	"""
		API function for state-date-total-data.

		This returns a JSON of dates and the number of infected people in all states for each day.

		Function returns (status, list_of_error)
		1 = All good
		-1 = Something died
	"""
	DATA_sdtd = {}
	states = []

	failList = []

	for row in data:
		# We need date and state. If I can't get them
		try:
			DateUpdated = str(row[0])
		except:
			failList.append("BigDataBox.utils.website.state_date_total_data.state_date_total_data: DateUpdated. Could not convert to string.")
			continue

		try:
			stateName = str(row[2])
		except:
			failList.append("BigDataBox.utils.website.state_date_total_data.state_date_total_data: stateName. Could not convert to string.")
			continue

		try:
			infected = int(row[4])
		except:
			infected = 0

		# We don't have this date recorded, hence we create a new entry
		if DateUpdated not in DATA_sdtd:
			DATA_sdtd[DateUpdated] = {}

			# Copy existing states into this entry
			for state in states:
				DATA_sdtd[DateUpdated][state] = 0

		# I legit forgot how this works. It works and that's all that matters.
		if stateName not in states:
			states.append(stateName)
			for dateKey in DATA_sdtd:
				DATA_sdtd[dateKey][stateName] = 0
		DATA_sdtd[DateUpdated][stateName] += infected
		
	with open(DIR_DATA + "APIData/state_date_total_data.json", 'w') as FPtr:
		dump(DATA_sdtd, FPtr)

	if len(failList) != 0:
		return (-1, failList)

	return (1, None)

