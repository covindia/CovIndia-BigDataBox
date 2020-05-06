"""
	This slave's daily motivation: https://www.youtube.com/watch?v=aqmhzwSU12I
	I urge you to check it out. Like seriously, you're going through this code, why the heck not?

	It's not a Rick-Roll.

	Author: IceCereal and not Rick Astley
"""

from json import dump

DIR_DATA = "../data/"

def district_values(DATA_general, testing : bool = None):
	"""
		The API function for present-district-values.

		This returns a JSON of real time stats of districts.

		Function returns (status, list_of_error)
		1 = All good
		-1 = Something died
	"""

	if not testing:
		with open(DIR_DATA + "APIData/present_district_values.json", 'w') as FPtr:
			dump(DATA_general, FPtr)

	return (1, None)

	# Yeah, that's it. So what?
