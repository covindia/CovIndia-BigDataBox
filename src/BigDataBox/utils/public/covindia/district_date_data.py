"""
	https://www.youtube.com/watch?v=8ZtInClXe1Q is the video that drives this slave.
	
	Red Shirt Man is it's favorite youtuber. It's always wanted to make a password storing algorithm, but
	after watchin Red Shirt Man's video about this, it had second thoughts.

	Red Shirt Man, you have saved the passwords of millions of people because if it weren't for you, this
	slave would have implemented it's own plaintext password storing hodge-bodge. #RedShirtMan4Eva

	Author: Red Shirt Man's biggest fan, IceCereal
"""

from json import dump
from datetime import datetime
from collections import OrderedDict

DIR_DATA = "../data/"

def district_date_data(data):
	"""
		The API function for covindia-district-date-data. Saves output to DIR_DATA / PublicData / covindia_district_date_data.json
	"""
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
			local_ddtd_total[district]["death"] = 0

		if DateUpdated not in DATA_ddtd:
			DATA_ddtd[DateUpdated] = {}
			for district in local_ddtd_total:
				DATA_ddtd[DateUpdated][district] = {}
				DATA_ddtd[DateUpdated][district]["infected"] = local_ddtd_total[district]["infected"]
				DATA_ddtd[DateUpdated][district]["death"] = local_ddtd_total[district]["death"]

		if district not in DATA_ddtd[DateUpdated]:
			DATA_ddtd[DateUpdated][district] = {}
			DATA_ddtd[DateUpdated][district]["infected"] = 0
			DATA_ddtd[DateUpdated][district]["death"] = 0

		if not (row[5] == '' or row[5] == ""):
			try:
				DATA_ddtd[DateUpdated][district]["infected"] += int(row[5])
				local_ddtd_total[district]["infected"] += int(row[5])
			except:
				DATA_ddtd[DateUpdated][district]["infected"] += 0
				local_ddtd_total[district]["infected"] += 0

		try:
			if not (row[6] == '' or row[6] == ""):
				DATA_ddtd[DateUpdated][district]["death"] += int(row[6])
				local_ddtd_total[district]["death"] += int(row[6])
		except:
			DATA_ddtd[DateUpdated][district]["death"] += 0
			local_ddtd_total[district]["death"] += 0

	with open(DIR_DATA + "PublicData/covindia_district_date_data.json", 'w') as FPtr:
		dump(DATA_ddtd, FPtr)

	return 1
