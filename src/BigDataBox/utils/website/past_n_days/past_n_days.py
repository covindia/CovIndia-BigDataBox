"""
	Get Past-N Days of Data

	Author: Jayesh
"""

import pandas as pd
import json
import requests
from datetime import date, datetime, timezone, timedelta
import math

DIR_DATA = "../data"

def decibel(X):
	"""
		Utility Function of a Utility Function to calculate:
			returns 10.0 * log (base 10) (X)
	"""
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
	past_days(14, "past_two_weeks.json")
	

def past_days(days : int, output_file : str):
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

	if days > 0:
		maximum_inf = decibel(df['infected'].max())

		X1 = inverse_decibel(1 * maximum_inf, 3)
		X2 = inverse_decibel(2 * maximum_inf, 3)

		out["splitPoints"] = [1, X1, X2, int(df['infected'].max())]

	for ix in df.index:
		out[df['district'][ix]] = {}
		out[df['district'][ix]]['infected'] = str(df['infected'][ix])
		out[df['district'][ix]]['dead'] = str(df['death'][ix])
		out[df['district'][ix]]['state'] = str(df['state'][ix])
		if df['infected'][ix] != 0 :
			out[df['district'][ix]]['value'] = str((10*math.log(df['infected'][ix],10))/max_infected_db)
		else :
			out[df['district'][ix]]['value'] = str(-1)

	with open(DIR_DATA + "/APIData/" + output_file, 'w') as f:
		json.dump(out,f)  

	return 1
