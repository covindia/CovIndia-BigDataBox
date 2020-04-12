"""
	Ah yes, the minion that quietly does it's work whenever called. This little bad boy of ours can crunch data and saves them
	to our data/ directory. It also does the magic of inserting stuff into HTML

	Minion's daily motivation:
		This youtube video explaining the beauty of life. This video, according to the minion, captures the essence
		of life, the universe and everything. The minion believes that this video is fundamental to the universe just as you and I are made
		up of atoms. As you can see, this video is everything to the minion. Please make sure that YouTube never takes it down because if
		YouTube was going to let us down, I don't know what minion would do:
		https://www.youtube.com/watch?v=dQw4w9WgXcQ

	Author: IceCereal + achal.ochod
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from json import dump, load
import copy

# Yes, the minion has it's own slaves to work.
# I, Cereal God, urge you to go through their code and see their interests.
# #SlavesLivesMattersAndSoDoTheirInterests

from BigDataBox.utils.website.daily.dates import daily_dates
from BigDataBox.utils.website.latest_updates.latest_updates import latest_updates_V2
from BigDataBox.utils.website.general.general import general
from BigDataBox.utils.website.general.district_values import district_values
from BigDataBox.utils.website.daily.states_complete import daily_states_complete
from BigDataBox.utils.website.state_date_total_data.state_date_total_data import state_date_total_data
from BigDataBox.utils.website.states_affected_numbers.states_affected_numbers import states_affected_numbers
from BigDataBox.utils.website.general.district_date_total_data import district_date_total_data

# Raw-Data
from BigDataBox.utils.public.covindia.raw_data import raw_data
# Present-State-Data
from BigDataBox.utils.public.covindia.state_data import state_data
# Present-General-Data
from BigDataBox.utils.public.covindia.general_data import general_data
# History-District-Data
from BigDataBox.utils.public.covindia.district_date_data import district_date_data

# Directories
DIR_DATA = "../data/"
DIR_RES = "res/"
DIR_PRODUCTION = "live/"

def do_your_work():
	"""
		Get the damn data from our google sheet and crunch these numbers.
		Store the numbers in your DIR_DATA, slave.
	"""

	scope = ['https://spreadsheets.google.com/feeds']
	creds = ServiceAccountCredentials.from_json_keyfile_name(DIR_RES + 'creds.json',scope)
	client = gspread.authorize(creds)
	with open(DIR_RES + "URL", 'r') as F:
		URL = F.read()
	sheet = client.open_by_url(URL).worksheet('Sheet1')

	data = sheet.get()
	data = data[1:]

	FAILLIST = []

	print ("Computing daily-dates...")
	dataCopy = copy.deepcopy(data)
	flag, failList = daily_dates(dataCopy)

	if flag == -1:
		FAILLIST.append(i for i in failList)

	print ("Computing daily-states-complete...")
	flag, failList = daily_states_complete(data)

	if flag == -1:
		FAILLIST.append(i for i in failList)

	print ("Computing general...")
	DATA_general = general(data)

	print ("Computing latest-updates...")
	flag, failList = latest_updates_V2(data, 5)

	if flag == -1:
		FAILLIST.append(i for i in failList)

	print ("Computing district-values...")
	flag, failList = district_values(DATA_general)

	if flag == -1:
		FAILLIST.append(i for i in failList)

	print ("Computing state-date-total-data...")
	flag, failList = state_date_total_data(data)

	if flag == -1:
		FAILLIST.append(i for i in failList)

	print ("Computing states-affected-numbers...")
	flag, failList = states_affected_numbers(data)

	if flag == -1:
		FAILLIST.append(i for i in failList)

	print ("Computing district-date-total-data...")
	dataCopy = copy.deepcopy(data)
	flag, failList = district_date_total_data(dataCopy)

	if flag == -1:
		FAILLIST.append(i for i in failList)

	print (FAILLIST)

	# TODO: Handle faillist and send it to overlord

	print ("Public:")
	print ("Computing covindia-raw-data...")
	raw_data(data)

	print ("Computing covindia-present-state-data...")
	state_data(data)

	print ("Computing covindia-present-general-data...")
	general_data(data)

	print ("Computing covindia-history-district-data...")
	dataCopy = copy.deepcopy(data)
	district_date_data(dataCopy)

if __name__ == "__main__":
	do_your_work()
