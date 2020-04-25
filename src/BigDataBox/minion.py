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

from BigDataBox.utils.website.daily.dates import daily_dates
from BigDataBox.utils.website.latest_updates.latest_updates import latest_updates_V2
from BigDataBox.utils.website.general.general import general
from BigDataBox.utils.website.general.district_values import district_values
from BigDataBox.utils.website.daily.states_complete import daily_states_complete
from BigDataBox.utils.website.state_date_total_data.state_date_total_data import state_date_total_data
from BigDataBox.utils.website.states_affected_numbers.states_affected_numbers import states_affected_numbers
from BigDataBox.utils.website.general.district_date_total_data import district_date_total_data
from BigDataBox.utils.website.zone_data.zone_data import zone_data
from BigDataBox.utils.website.past_n_days.past_n_days import past_n_days
from BigDataBox.utils.website.testing_data.testing_data import testing_data

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

	if testing == True:
		# Sample Data
		data = [
			['Date', 'Time', 'State', 'District', 'confirmed +ve', 'Dead', 'Source link'], 
			['13/03/2020', '14:10', 'Uttar Pradesh', 'GBN_Faridabad', '1', '', 'https://www.hindustantimes.com/delhi-news/executive-of-noida-firm-living-in-delhi-tests-positive-for-coronavirus-official/story-QuRmbRHRT4OFRMsodyiaEP.html'],
			['04/03/2020', '21:37', 'Haryana', 'Gurgaon', '14', '', 'https://news.abplive.com/videos/news/haryana-govt-declares-coronavirus-as-epidemic-1174072'],
			['04/03/2020', '21:37', 'Rajasthan', 'Jaipur', '1'],
			['12/03/2020', '14:26', 'Uttar Pradesh', 'Lucknow', '1', '', 'https://www.mohfw.gov.in/pdf/DistrictWiseList324.pdf'],
			['12/03/2020', '14:26', 'Uttar Pradesh', 'GBN_Faridabad', '1', '', 'https://www.mohfw.gov.in/pdf/DistrictWiseList324.pdf'],
			['13/03/2020', '14:26', 'Uttar Pradesh', 'Ghaziabad', '2', '', 'https://www.mohfw.gov.in/pdf/DistrictWiseList324.pdf'],
			['13/03/2020', '14:26', 'Uttar Pradesh', 'Agra', '7', '', 'https://www.mohfw.gov.in/pdf/DistrictWiseList324.pdf'],
			['13/03/2020', '22:01', 'Jammu and Kashmir', 'Jammu', '1', '', 'https://twitter.com/diprjk/status/1238438565027045383?s=20'],
			['13/03/2020', '21:37', 'Jammu and Kashmir', 'Jammu', '1', '', 'https://twitter.com/diprjk/status/1238438565027045383?s=20'],
			['10/03/2020', '21:32', 'Karnataka', 'Gulbarga', '1', '1', 'https://economictimes.indiatimes.com/news/politics-and-nation/man-suspected-of-coronavirus-dies-after-returning-from-saudi-arabia/articleshow/74574771.cms'],
			['13/03/2020', '20:17', 'Kerala', 'Thiruvananthapuram', '3', '', 'https://www.financialexpress.com/lifestyle/health/coronavirus-live-news-coronavirus-latest-updates-coronavirus-symptoms-visa-air-india-delhi-coronavirus-hyderabad-kerala-bangalore-coronavirus-symptoms-treatment/1895511/'],
			['12/03/2020', '0:00', 'Andhra Pradesh', 'Sri_Potti_Sriramulu_Nellore', '1', '', 'https://twitter.com/RajivKrishnaS/status/1240644921423310849?s=20'],
			['13/03/2020', '9:10', 'Karnataka', 'Bangalore', '1', '', 'https://twitter.com/BollyNumbers/status/1242148572734210048/photo/1'],
			['11/03/2020', '16:09', 'Maharashtra', 'Nagpur', '1', '', 'https://www.firstpost.com/health/coronavirus-outbreak-live-updates-covid-19-who-pandemic-quarantine-india-noida-bangalore-cases-alert-novel-latest-news-today-ipl-school-college-8138611.html'],
			['10/03/2020', '22:12', 'Karnataka', 'Bangalore', '3', '', 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_India'],
			['10/03/2020', '0:00', 'Kerala', 'Pathanamthitta', '2', '', 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_India'],
			['10/03/2020', '0:00', 'Kerala', 'Kottayam', '2', '', 'https://www.mohfw.gov.in/pdf/DistrictWiseList324.pdf'],
			['10/03/2020', '0:00', 'Maharashtra', 'Thane', '5', '', 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_India'],
			['09/03/2020', '0:00', 'Karnataka', 'Bangalore', '1', '', 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_India'],
			['08/03/2020', '0:00', 'Kerala', 'Pathanamthitta', '5', '', 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_India'],
			['02/03/2020', '19:53', 'Telangana', 'Hyderabad', '5'],
			['03/02/2020', '0:00', 'Kerala', 'Kannur', '1', '', 'http://dhs.kerala.gov.in/%e0%b4%a1%e0%b5%86%e0%b4%af%e0%b4%bf%e0%b4%b2%e0%b4%bf-%e0%b4%ac%e0%b5%81%e0%b4%b3%e0%b5%8d%e0%b4%b3%e0%b4%b1%e0%b5%8d%e0%b4%b1%e0%b4%bf%e0%b4%a8%e0%b5%8d%e2%80%8d/'],
			['07/03/2020', '9:38', 'Tamil Nadu', 'Kancheepuram', '1', '', 'https://twitter.com/BollyNumbers/status/1242151071029448714?s=20'],
			['02/03/2020', '0:00', 'Delhi', 'Delhi', '1', '', 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_India'],
			['02/03/2020', '0:00', 'Delhi', 'Delhi', '5', '', 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_India'],
			['02/03/2020', '0:00', 'Delhi', 'Delhi', '1', '', 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_India'],
			['13/03/2020', '0:00', 'Delhi', 'Delhi', '', '1', 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_India'],
			['13/03/2020', '0:00', 'Tamil Nadu', 'DIST_NA', '', '1', 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_India'],
			['10/03/2020', '16:25', 'Rajasthan', 'Jaipur', '1', '', 'https://www.deccanherald.com/national/anti-hiv-drugs-given-to-treat-coronavirus-affected-elderly-italian-couple-in-jaipur-812356.html'],
			['13/03/2020', '0:00', 'Maharashtra', 'Nagpur', '2', '', 'https://arogya.maharashtra.gov.in/1175/Novel--Corona-Virus']
		]
	else:
		# Not testing
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
	flag, failList = daily_dates(dataCopy, testing)

	if flag == -1:
		FAILLIST.append(i for i in failList)

	print ("Computing daily-states-complete...")
	flag, failList = daily_states_complete(data, testing)

	if flag == -1:
		FAILLIST.append(i for i in failList)

	print ("Computing general...")
	DATA_general = general(data, testing)

	print ("Computing latest-updates...")
	flag, failList = latest_updates_V2(data, 5, testing)

	if flag == -1:
		FAILLIST.append(i for i in failList)

	print ("Computing district-values...")
	flag, failList = district_values(DATA_general, testing)

	if flag == -1:
		FAILLIST.append(i for i in failList)

	print ("Computing state-date-total-data...")
	flag, failList = state_date_total_data(data, testing)

	if flag == -1:
		FAILLIST.append(i for i in failList)

	print ("Computing states-affected-numbers...")
	flag, failList = states_affected_numbers(data, testing)

	if flag == -1:
		FAILLIST.append(i for i in failList)

	print ("Computing district-date-total-data...")
	dataCopy = copy.deepcopy(data)
	flag, failList = district_date_total_data(dataCopy, testing)

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

	print("Computing testing-data")
	testing_data(testing)

	print ("\nFaillist:", FAILLIST)
	# TODO: Handle faillist and send it to overlord

if __name__ == "__main__":
	do_your_work()
