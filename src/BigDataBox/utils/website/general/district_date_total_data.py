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

DIR_DATA = "../data/"

def district_date_total_data(original_data):
	"""
		The API function for district-date-total-data. Saves output to DIR_DATA / APIData / district_date_total_data.json
	"""
	data = original_data[:]
	DATA_ddtd = OrderedDict()
	local_ddtd_total = {}

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
			continue

		if district == "DIST_NA":
			continue

		try:
			DateUpdated = str(row[1])
		except:
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
			try:
				DATA_ddtd[DateUpdated][district]["infected"] += 0
				local_ddtd_total[district]["infected"] += 0
			except:
				DATA_ddtd[DateUpdated][district]["infected"] = 0
				local_ddtd_total[district]["infected"] = 0

		try:
			DATA_ddtd[DateUpdated][district]["dead"] += int(row[6])
			local_ddtd_total[district]["dead"] += int(row[6])
		except:
			try:
				DATA_ddtd[DateUpdated][district]["dead"] += 0
				local_ddtd_total[district]["dead"] += 0
			except:
				DATA_ddtd[DateUpdated][district]["dead"] = 0
				local_ddtd_total[district]["dead"] = 0
	for date in DATA_ddtd:
		# find the max value in DATA_ddtd
		maxINF = 0
		totalINF = 0
		for district in DATA_ddtd[date]:
			totalINF += DATA_ddtd[date][district]["infected"]

			if DATA_ddtd[date][district]["infected"] > maxINF:
				maxINF = DATA_ddtd[date][district]["infected"]

		for district in DATA_ddtd[date]:
			DATA_ddtd[date][district]["value"] = DATA_ddtd[date][district]["infected"] / maxINF

		DATA_ddtd[date]["total-infected"] = totalINF
		DATA_ddtd[date]["max-legend-value"] = maxINF

	with open(DIR_DATA + "APIData/district_date_total_data.json", 'w') as FPtr:
		dump(DATA_ddtd, FPtr)

	return 1
	# Yeet, Skeet and Repeet
