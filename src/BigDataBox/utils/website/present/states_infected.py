"""
	This slave's daily motivation: https://www.youtube.com/watch?v=_3ngiSxVCBs

	Man, the goddamn memories. Makes me wanna cry.
	Those were the good days. When I spent 6 - 10 hours after class playing Memekraft.
	Why do I have to be away from my desktop :_(.

	Special shoutout to my favorite world: RageQuit. You'll always be in my heart, oh easily hundreds-of-hours-spent-on world.

	Author: IceCereal
"""

from json import dump

DIR_DATA = "../data/"

def states_infected(data_new, testing : bool = None):
	"""
		The API function for present-states-infected.

		This returns a JSON of the tally of number of infections in each state.

		Function returns (status, list_of_error)
		1 = All good
		-1 = Something died
	"""

	failList = []

	DATA_present_states_infected = {}
	for row in data_new:
		try:
			state = str(row[2])
		except:
			print ("extracting state name failed .... {", row, "}")
			failList.append("BigDataBox.utils.website.present.states_infected: stateName. Could not extract state name {" + row + "}" )
			return (-1 ,failList)

		try:
			DATA_present_states_infected[state] += int(row[4])
		except:
			try:
				DATA_present_states_infected[state] += 0
			except:
				if row[4] == "":
					DATA_present_states_infected[state] = 0
				else:
					DATA_present_states_infected[state] = int(row[4])

	if not testing:
		with open(DIR_DATA + "APIData/present_states_infected.json", 'w') as FPtr:
			dump(DATA_present_states_infected, FPtr)

	return (1, None)
