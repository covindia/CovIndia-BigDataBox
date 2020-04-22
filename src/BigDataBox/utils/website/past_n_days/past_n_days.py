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