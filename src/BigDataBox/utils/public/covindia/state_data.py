"""
	A weeb and a piano enthusiast, there's no doubt that https://www.youtube.com/watch?v=sEQf5lcnj_o is
	this slave's daily motivation.

	It's from a good anime and the OP too is realllllly good. It makes the slave tear up everytime. Gosh,
	what a drama queen :eye-roll:.

	(Secretly agrees too)

	Author: Ghoul IceCereal
"""

from json import dump

DIR_DATA = "../data/"

def state_data(data):
	"""
		The API function for state-data. Saves output to DIR_DATA / PublicData / covindia_state_data.json
	"""

	DATA_sd = {}
	for row in data:
		try:
			state = str(row[2])
		except:
			print ("extracting state name failed .... {", row, "}")
			state = "NA"

		if state not in DATA_sd:
			DATA_sd[state] = 0

		try:
			DATA_sd[state] += int(row[4])
		except:
			pass

	# UNCOMMENT THIS IF YOU WANT TO STILL USE A DEPRECATED FUNCTION, GODDAMNIT
	with open(DIR_DATA + "PublicData/covindia_state_data.json", 'w') as FPtr:
		dump(DATA_sd, FPtr)

	return 1
