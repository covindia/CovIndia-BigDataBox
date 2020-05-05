"""
	This slave's daily motivation: https://youtu.be/4v8ek9TEeOU?t=40

	This video makes this lil dude laugh like crazy. You should see the slave laugh.
	Pffftt.... it thinks it has freedom. :evil-overlord-vibes:

	It literally goes UwU when it laughs. UwU? More like eww. :eyes-roll:

	Author: IceCereal
"""

import copy
from json import dump
from datetime import datetime
from collections import OrderedDict

DIR_DATA = "../data/"

def infected_daily(data_old_sheet, testing : bool = None):
	"""
		The API function for history-infected-daily.

		This returns a JSON that gives the number of infected people on that day.

		Function returns (status, list_of_error)
		1 = All good
		-1 = Something died
	"""
	DATA_history_infected_daily = OrderedDict()

	dateToday = datetime.today().date()

	data_pruned = []

	# NOTE: By doing this, I have reduced a O(n^2) algo to a O(n) algo.
	# NOTE to the reader: Attend your algos classes. They help.
	for row in data_old_sheet:
		temp_row = copy.deepcopy(row)
		Date = datetime.strptime(str(row[0]), "%d/%m/%Y")
		if Date.date() != dateToday:
			temp_row.insert(0, Date)
			data_pruned.append(temp_row)

	# However, sorting is still a O(n*log(n)), so overall complexity remains to be O(n*log(n))
	data_pruned.sort()

	for row in data_pruned:
		date = str(row[1])

		cutoff = datetime(2020, 3, 1)
		if datetime.strptime(date, "%d/%m/%Y") > cutoff:

			# If date already exists in the dictionary
			if str(date) in DATA_history_infected_daily:
				try:
					# Add the number of cases to the dictionary
					DATA_history_infected_daily[str(date)] += int(row[5])
				except:
					# For cases where row[5] == '' or ""
					DATA_history_infected_daily[str(date)] += 0

			# If date doesn't exist in the dictionary, i.e. new date
			else:
				try:
					# Set it to the number inside the cell
					DATA_history_infected_daily[str(date)] = int(row[5])
				except:
					# For cases where row[5] == '' or ""
					DATA_history_infected_daily[str(date)] = 0

	if not testing:
		with open(DIR_DATA + "APIData/history_infected_daily.json", 'w') as FPtr:
			dump(DATA_history_infected_daily, FPtr)

	return (1, None)
