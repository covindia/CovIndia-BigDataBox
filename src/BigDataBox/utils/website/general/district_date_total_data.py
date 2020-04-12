"""
	The video that drives this slave: https://www.youtube.com/watch?v=kXShLPXfWZA
	
	ATLA holds a special place in this slave's heart. It remembers watching ATLA as a child and remembers the
	beautiful animations, story, music, morals and values. Uncle Iroh is no doubt it's favorite character. The
	first thing that this slave recommends to *anyone* who asks for a recommendation is ATLA. It says, and I
	quote, "It might look like a cartoon. However, it's a proper TV show that impacted millions of people. The
	awesome animations, the incredible story, and just about everything there is to it is why ATLA is the best
	TV show in my opinion".

	Have to say, it's hard to argue with this slave.

	Author: Firelord IceCereal
"""

from json import dump
from datetime import datetime
from collections import OrderedDict
from math import log10

DIR_DATA = "../data/"

def decibel(X):
	"""
		Utility Function of a Utility Function to calculate:
			returns 10.0 * log (base 10) (X)
	"""
	if X == 0:
		return 0
	if X == 1:
		return 0.000001
	return (10.0 * log10 (X))

def inverse_decibel(X, split_number):
	"""
		The inverse of the decibel function. I.e., if you know the db value
		and you want to calculate the number that gives you the db value.

		args:
			X (float) : The Decibel
			split_number (float) : The number splits wanted in the legend

		returns:
			inv_dec (int) : The inverse_decibel value
	"""
	return int(10 ** (X / (10 * split_number)))

def district_date_total_data(original_data):
	"""
		The API function for district-date-total-data.

		This returns a JSON that gives all the data of affected districts on all previous dates.

		Function returns (status, list_of_error)
		1 = All good
		-1 = Something died
	"""
	data = original_data[:]
	DATA_ddtd = OrderedDict()
	local_ddtd_total = {}

	failList = []

	# NOTE: By doing this, I have reduced a O(n^2) algo to a O(n) algo.
	# NOTE to the reader: Attend your algos classes. They help.
	for row in data:
		Date = datetime.strptime(str(row[0]), "%d/%m/%Y")
		row.insert(0, Date)

	# However, sorting is still a O(n*log(n)), so overall complexity remains to be O(n*log(n))
	data.sort()

	for row in data:
		try:
			district = row[4]
		except:
			failList.append("BigDataBox.utils.website.district_date_total_data.district_date_total_data: district. Could not extract district name {" + str(row) + "}" )
			continue

		try:
			DateUpdated = str(row[1])
		except:
			failList.append("BigDataBox.utils.website.district_date_total_data.district_date_total_data: DateUpdated. Could not extract date updated {" + str(row) + "}" )
			continue

		if district not in local_ddtd_total:
			local_ddtd_total[district] = {}
			local_ddtd_total[district]["infected"] = 0
			local_ddtd_total[district]["dead"] = 0

		if DateUpdated not in DATA_ddtd:
			DATA_ddtd[DateUpdated] = {}
			for district in local_ddtd_total:
				DATA_ddtd[DateUpdated][district] = {}
				DATA_ddtd[DateUpdated][district]["infected"] = local_ddtd_total[district]["infected"]
				DATA_ddtd[DateUpdated][district]["dead"] = local_ddtd_total[district]["dead"]

		if district not in DATA_ddtd[DateUpdated]:
			DATA_ddtd[DateUpdated][district] = {}
			DATA_ddtd[DateUpdated][district]["infected"] = 0
			DATA_ddtd[DateUpdated][district]["dead"] = 0

		try:
			DATA_ddtd[DateUpdated][district]["infected"] += int(row[5])
			local_ddtd_total[district]["infected"] += int(row[5])
		except:
			DATA_ddtd[DateUpdated][district]["infected"] += 0
			local_ddtd_total[district]["infected"] += 0

		try:
			DATA_ddtd[DateUpdated][district]["dead"] += int(row[6])
			local_ddtd_total[district]["dead"] += int(row[6])
		except:
			DATA_ddtd[DateUpdated][district]["dead"] += 0
			local_ddtd_total[district]["dead"] += 0

	for date in DATA_ddtd:
		# find the max value in DATA_ddtd
		maxINF = 0
		totalINF = 0

		# For now, value is calculated as decibels.
		#
		# It was previously linear which had the problem with an outlier (with a very high infected number).
		# It diminished the value of other districts.

		# Step 1. Calculate the raw decibels and keep track of the highest

		highestValue = 0

		for district in DATA_ddtd[date]:
			# Get total infected & max infected
			totalINF += DATA_ddtd[date][district]["infected"]

			if DATA_ddtd[date][district]["infected"] > maxINF:
				maxINF = DATA_ddtd[date][district]["infected"]

			# Calculate decibels
			districtValue = decibel(DATA_ddtd[date][district]["infected"])

			if districtValue > highestValue:
				highestValue = districtValue

			DATA_ddtd[date][district]["value"] = districtValue

		# Step 2. Make all the values divided by highestValue [To get numbers between 0 & 1]
		for district in DATA_ddtd[date]:
			DATA_ddtd[date][district]["value"] = DATA_ddtd[date][district]["value"] / highestValue

		# Step 3. Calculate the 2 points that correspond to highestValue/3 and 2*highestValue/3
		#
		# If 10 log10 (X1) = highestValue/3
		# Then X1 = 10 ^ (highestValue/30)
		#
		# If 10 log10 (X2) = 2*highestValue/3
		# Then X2 = 10 ^ (2*highestValue/30)

		X1 = inverse_decibel(1 * highestValue, 3)
		X2 = inverse_decibel(2 * highestValue, 3)

		DATA_ddtd[date]["total-infected"] = totalINF
		DATA_ddtd[date]["max-legend-value"] = maxINF
		DATA_ddtd[date]["splitPoints"] = [1, X1, X2, maxINF]

	with open(DIR_DATA + "APIData/district_date_total_data.json", 'w') as FPtr:
		dump(DATA_ddtd, FPtr)

	if len(failList) != 0:
		return (-1, failList)

	return (1, failList)
	# Yeet, Skeet and Repeet
