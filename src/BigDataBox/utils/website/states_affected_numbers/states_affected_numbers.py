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

def states_affected_numbers(data, testing : bool = None):
	"""
		The API function for states-affected-numbers.

		This returns a JSON of the tally of number of infections in each state.

		Function returns (status, list_of_error)
		1 = All good
		-1 = Something died
	"""

	failList = []

	DATA_states_affected_number = {}
	for row in data:
		try:
			state = str(row[2])
		except:
			print ("extracting state name failed .... {", row, "}")
			failList.append("BigDataBox.utils.website.state_affected_numbers.state_affected_numbers: stateName. Could not extract state name {" + row + "}" )
			return (-1 ,failList)

		try:
			DATA_states_affected_number[state] += int(row[4])
		except Exception as e:
			try:
				DATA_states_affected_number[state] += 0
			except:
				if row[4] == "":
					DATA_states_affected_number[state] = 0
				else:
					DATA_states_affected_number[state] = int(row[4])

	if not testing:
		with open(DIR_DATA + "APIData/states_affected_numbers.json", 'w') as FPtr:
			dump(DATA_states_affected_number, FPtr)

	return (1, None)
