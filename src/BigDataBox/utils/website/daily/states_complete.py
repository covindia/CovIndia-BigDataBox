"""
	Originally: utils.states_affected_numbers.states_affected_numbers (DEPRECATED)
	
	This slave's daily motivation: https://www.youtube.com/watch?v=_3ngiSxVCBs

	Man, the goddamn memories. Makes me wanna cry.
	Those were the good days. When I spent 6 - 10 hours after class playing Memekraft.
	Why do I have to be away from my desktop :_(.

	Special shoutout to my favorite world: RageQuit. You'll always be in my heart, oh easily hundreds-of-hours-spent-on world.

	Author: IceCereal
"""

from json import dump
from datetime import datetime

DIR_DATA = "../data/"

def daily_states_complete(data, testing : bool = None):
	"""
		The API function for daily-states-complete.

		This returns a JSON that gives stats about states today, i.e. number of new cases today vs total number of cases and
		same with deaths.

		Function returns (status, list_of_error)
		1 = All good
		-1 = Something died
	"""
	DATA_daily_states_complete = {}
	baseDate = datetime.combine(datetime.now().date(), datetime.min.time())

	failList = []

	for row in data:
		try:
			DateUpdated = str(row[0])
		except:
			DateUpdated = datetime.now().strftime("%d/%m/%Y")

		try:
			TimeUpdated = str(row[1])
		except:
			TimeUpdated = "00:00"

		try:
			state = str(row[2])
		except:
			failList.append("BigDataBox.utils.website.daily.states_complete: state. Could not extract state name {" + row + "}" )
			continue

		try:
			infected = int(row[4])
		except:
			infected = 0

		try:
			dead = int(row[5])
		except:
			dead = 0


		DateUpdated_Compare = datetime.combine(datetime.strptime(DateUpdated, "%d/%m/%Y"), datetime.strptime(TimeUpdated, "%H:%M").time())

		if state not in DATA_daily_states_complete:
			DATA_daily_states_complete[state] = {
				"TotalCases" : 0,
				"NewCases" : 0,
				"TotalDeaths" : 0,
				"NewDeaths" : 0
			}

		DATA_daily_states_complete[state]["TotalCases"] += infected
		DATA_daily_states_complete[state]["TotalDeaths"] += dead

		if DateUpdated_Compare > baseDate:
			# This is today's data, woop woop
			DATA_daily_states_complete[state]["NewCases"] += infected
			DATA_daily_states_complete[state]["NewDeaths"] += dead

	if not testing:
		with open(DIR_DATA + "APIData/daily_states_complete.json", 'w') as FPtr:
			dump(DATA_daily_states_complete, FPtr)

	if len(failList) != 0:
		return (-1, failList)

	return (1, None)
