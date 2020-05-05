"""
	Get Past-24 Hours of Data

	Latest Version Author: IceCereal
	Legacy Author: Jayesh
"""

from datetime import datetime
from json import dump, load

DIR_DATA = "../data"

def twenty_four_hours(data_new, testing : bool = None):
	"""
		The API function for past-twenty-four-hours.

		This returns a JSON that gives the number of new_infected, new_deaths, new_value, states
		per district.

		Function returns (status, list_of_error)
		1 = All good
		-1 = Something died
	"""
	DATA_24_hours = {}

	timeNow = datetime.now()

	failList = []

	for row in data_new:
		try:
			date_updated = datetime.strptime(str(row[0])+" "+str(row[1]), "%d/%m/%Y %H:%M")
		except:
			failList.append("Passed in website.history.twenty_four_hours:" + str(row[0])+" "+str(row[1]))
			continue
		
		time_elapsed = timeNow - date_updated
		
		if time_elapsed.days > 1:
			continue

		try:
			district = str(row[3])
		except:
			continue

		try:
			state = str(row[2])
		except:
			continue

		try:
			infected = int(row[4])
		except:
			infected = 0

		try:
			dead = int(row[5])
		except:
			dead = 0

		if district not in DATA_24_hours:
			DATA_24_hours[district] = {
				"newInfected" : 0,
				"newDeaths" : 0,
				"state" : None,
				"value" : 0
			}

		DATA_24_hours[district]["newInfected"] += infected
		DATA_24_hours[district]["newDeaths"] += dead
		DATA_24_hours[district]["state"] = state # Possible TODO: assert state is the same

	if not testing:
		with open(DIR_DATA + "/APIData/history_twenty_four_hours.json", 'w') as FPtr:
			dump(DATA_24_hours, FPtr)

	if len(failList) != 0:
		return (-1, failList)

	return (1, None)

############################################################################
### BELOW THIS IS LEGACY CODE
### DO NOT TOUCH IT
############################################################################
def decibel(X):
	"""
		Utility Function of a Utility Function to calculate:
			returns 10.0 * log (base 10) (X)
	"""
	import math

	if X == 0:
		return 0
	if X == 1:
		return 0.000001
	return (10.0 * math.log10 (X))


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

def past_n_days(testing):
	if testing:
		return 1

	past_days(1, "past_twenty_four_hours.json")


def past_days(days : int, output_file : str):
	import pandas as pd
	import json
	import requests
	from datetime import date, datetime, timezone, timedelta

	url = 'https://v1.api.covindia.com/covindia-raw-data'
	raw_data = requests.get(url=url).json()

	raw_data = {int(old_key): val for old_key, val in raw_data.items()}
	raw_data_df = pd.DataFrame.from_dict(raw_data, orient='index')
	raw_data_df  = raw_data_df [['date','time','district','state','infected','death','source']]
	raw_data_df['datetime'] = raw_data_df['date'] + " " + raw_data_df['time']
	raw_data_df["datetime"] = pd.to_datetime(raw_data_df["datetime"],dayfirst=True)

	curr_dt = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30) # UTC time
	prev_dt = curr_dt + timedelta(hours=-24*days, minutes=0)
	curr_dt_string = curr_dt.strftime("%d/%m/%Y %H:%M:%S")
	prev_dt_string = prev_dt.strftime("%d/%m/%Y %H:%M:%S")

	cond = (raw_data_df['datetime'] < pd.to_datetime(curr_dt_string,dayfirst = True)) & (raw_data_df['datetime'] > pd.to_datetime(prev_dt_string,dayfirst = True))

	df_new = raw_data_df.loc[cond]# & (raw_data_df['date'] <= curr_dt_string.split()[0])]

	df = df_new.groupby(['district','state'],as_index = False)['infected','death'].sum()

	out = {}
	max_infected_db = 10*math.log(df['infected'].max(),10)

	if days != 1:
		maximum_inf = decibel(df['infected'].max())

		X1 = inverse_decibel(1 * maximum_inf, 3)
		X2 = inverse_decibel(2 * maximum_inf, 3)

		out["splitPoints"] = [1, X1, X2, int(df['infected'].max())]

	for ix in df.index:
		out[df['district'][ix]] = {}
		out[df['district'][ix]]['new_infected'] = str(df['infected'][ix])
		out[df['district'][ix]]['new_deaths'] = str(df['death'][ix])
		out[df['district'][ix]]['state'] = str(df['state'][ix])
		if df['infected'][ix] != 0 :
			out[df['district'][ix]]['value'] = str((10*math.log(df['infected'][ix],10))/max_infected_db)
		else :
			out[df['district'][ix]]['value'] = str(-1)

	with open(DIR_DATA + "/APIData/" + output_file, 'w') as f:
		json.dump(out,f)  

	return 1

### LEGACY CODE ENDS