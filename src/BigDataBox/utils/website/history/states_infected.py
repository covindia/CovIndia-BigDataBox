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

def states_infected(data_old, testing : bool = None):
	"""
		API function for history-states-infected.

		This returns a JSON of dates and the number of infected people in all states for each day.

		Function returns (status, list_of_error)
		1 = All good
		-1 = Something died
	"""
	DATA_si = {}
	states = []

	failList = []

	dateToday = datetime.today().date()

	for row in data_old:
		# We need date and state.
		try:
			DateUpdated_raw = str(row[0])
		except:
			failList.append("BigDataBox.utils.website.history.states_infected: DateUpdated. Could not convert to string.")
			continue

		DateUpdated_date = datetime.strptime(DateUpdated_raw, "%d/%m/%Y").date()
		if DateUpdated_date == dateToday:
			continue

		try:
			stateName = str(row[2])
		except:
			failList.append("BigDataBox.utils.website.history.states_infected: stateName. Could not convert to string.")
			continue

		try:
			infected = int(row[4])
		except:
			infected = 0

		# We don't have this date recorded, hence we create a new entry
		if DateUpdated_raw not in DATA_si:
			DATA_si[DateUpdated_raw] = {}

			# Copy existing states into this entry
			for state in states:
				DATA_si[DateUpdated_raw][state] = 0

		# I legit forgot how this works. It works and that's all that matters.
		if stateName not in states:
			states.append(stateName)
			for dateKey in DATA_si:
				DATA_si[dateKey][stateName] = 0
		DATA_si[DateUpdated_raw][stateName] += infected
		
	if not testing:
		with open(DIR_DATA + "APIData/history_states_infected.json", 'w') as FPtr:
			dump(DATA_si, FPtr)

	if len(failList) != 0:
		return (-1, failList)

	return (1, None)

