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

import copy
import gspread
from json import dump, load
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# Yes, the minion has it's own slaves to work.
# I, Cereal God, urge you to go through their code and see their interests.
# #SlavesLivesMattersAndSoDoTheirInterests

from BigDataBox.utils.website.history.infected_daily import infected_daily
from BigDataBox.utils.website.latest_updates.latest_updates import latest_updates_V2
from BigDataBox.utils.website.general.general import general
from BigDataBox.utils.website.present.district_values import district_values
from BigDataBox.utils.website.present.states_cases_deaths import states_cases_deaths
from BigDataBox.utils.website.history.states_infected import states_infected as history_states_infected
from BigDataBox.utils.website.present.states_infected import states_infected as present_states_infected
from BigDataBox.utils.website.history.districts_values import districts_values
from BigDataBox.utils.website.zone_data.zone_data import zone_data
from BigDataBox.utils.website.past_n_days.past_n_days import past_n_days
from BigDataBox.utils.website.testing_data.testing_data import testing_data
from BigDataBox.utils.website.cured_data.cured_data import cured_data
from BigDataBox.utils.website.csv.history.states_infected import states_infected as csv_history_states_infected

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

def do_your_work(testing : bool = None):
	"""
		Get the damn data from our google sheet and crunch these numbers.
		Store the numbers in your DIR_DATA, slave.
	"""

	scope = ['https://spreadsheets.google.com/feeds']
	creds = ServiceAccountCredentials.from_json_keyfile_name(DIR_RES + 'creds.json',scope)
	client = gspread.authorize(creds)
	with open(DIR_RES + "URLS.json", 'r') as F:
		urls = load(F)
	sheet_old = client.open_by_url(urls['Old-Sheet']).worksheet('Sheet1')
	sheet_new = client.open_by_url(urls['New-Sheet']).worksheet('Sheet1')
	sheet_cured = client.open_by_url(urls['Cured']).worksheet('Sheet1')
	sheet_testing = client.open_by_url(urls['Testing']).worksheet('Sheet1')

	data_old = sheet_old.get()
	data_new = sheet_new.get()
	data_cured = sheet_cured.get()
	data_testing = sheet_testing.get()
	
	# Remove Headers
	data_old = data_old[1:]
	data_new = data_new[1:]
	data_cured = data_cured[1:]
	data_testing = data_testing[1:]

	FAILLIST = []

	print ("Computing history-infected-daily...")
	dataCopy = copy.deepcopy(data_old)
	flag, failList = infected_daily(dataCopy, testing)

	print ("Computing present-states-cases-deaths...")
	flag, failList = states_cases_deaths(data_new, testing)

	print ("Computing general...")
	DATA_general = general(data_new, testing)

	print ("Computing latest-updates...")
	flag, failList = latest_updates_V2(data_new, 5, testing)

	print ("Computing present-district-values...")
	flag, failList = district_values(DATA_general, testing)

	print ("Computing history-states-infected...")
	flag, failList = history_states_infected(data_old, testing)

	print ("Computing present-states-infected...")
	flag, failList = present_states_infected(data_new, testing)

	print("Computing csv-history-states-infected")
	flag, failList = csv_history_states_infected(data_old, testing)

	print ("Computing history-districts-values...")
	dataCopy = copy.deepcopy(data_new)
	flag, failList = districts_values(dataCopy, testing)

	print("Computing testing-data")
	testing_data(testing)

	print("Computing cured-data")
	cured_data(testing)

	if flag == -1:
		FAILLIST.append(i for i in failList)

	print ("Computing zone-data")
	zone_data(testing)

	print ("\nPublic:")
	print ("Computing covindia-raw-data...")
	raw_data(data, testing)

	print ("Computing covindia-present-state-data...")
	state_data(data, testing)

	print ("Computing covindia-present-general-data...")
	general_data(data, testing)

	print ("Computing covindia-history-district-data...")
	dataCopy = copy.deepcopy(data)
	district_date_data(dataCopy, testing)

	print ("Computing past-n-days...")
	past_n_days(testing)

	print ("\nFaillist:", FAILLIST)
	# TODO: Handle faillist and send it to overlord

if __name__ == "__main__":
	do_your_work()
