"""
	This slave's daily motivation: https://youtu.be/4v8ek9TEeOU?t=40

	This video makes this lil dude laugh like crazy. You should see the slave laugh.
	Pffftt.... it thinks it has freedom. :evil-overlord-vibes:

	It literally goes UwU when it laughs. UwU? More like eww. :eyes-roll:

	Author: IceCereal
"""

from datetime import datetime
from json import dump
from collections import OrderedDict

DIR_DATA = "../data/"

def daily_dates(data_old_sheet, testing : bool = None):
	"""
		The API function for daily-dates.

		This returns a JSON that gives the number of infected people on that day.

		Function returns (status, list_of_error)
		1 = All good
		-1 = Something died
	"""
	DATA_daily_dates = OrderedDict()

	dateToday = datetime.today().date()

	# NOTE: By doing this, I have reduced a O(n^2) algo to a O(n) algo.
	# NOTE to the reader: Attend your algos classes. They help.
	for row in data_old_sheet:
		Date = datetime.strptime(str(row[0]), "%d/%m/%Y")
		if Date.date() != dateToday:
			row.insert(0, Date)

	# However, sorting is still a O(n*log(n)), so overall complexity remains to be O(n*log(n))
	data_old_sheet.sort()

	for row in data_old_sheet:
		date = str(row[1])

		cutoff = datetime(2020, 3, 1)
		if datetime.strptime(date, "%d/%m/%Y") > cutoff:

			# If date already exists in the dictionary
			if str(date) in DATA_daily_dates:
				try:
					# Add the number of cases to the dictionary
					DATA_daily_dates[str(date)] += int(row[5])
				except:
					# For cases where row[5] == '' or ""
					DATA_daily_dates[str(date)] += 0

			# If date doesn't exist in the dictionary, i.e. new date
			else:
				try:
					# Set it to the number inside the cell
					DATA_daily_dates[str(date)] = int(row[5])
				except:
					# For cases where row[5] == '' or ""
					DATA_daily_dates[str(date)] = 0

	if not testing:
		with open(DIR_DATA + "APIData/daily_dates.json", 'w') as FPtr:
			dump(DATA_daily_dates, FPtr)

	return (1, None)
