import flask
from flask import jsonify, request, escape, send_file
from json import load, dump
from datetime import datetime
import os

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import gspread
from oauth2client.service_account import ServiceAccountCredentials

DIR_DATA = os.environ['DATA_REPO_PATH']

# Set the connection between GSheets and this server

app = flask.Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
limiter = Limiter(
	app,
	key_func=get_remote_address
)

@app.route('/', methods=['GET'])
def home():
	return "<a href=\"https://covindia.com\">Click here to go to https://covindia.com</a>. You were not supposed to stumble here.<br><br>But now that you did, hello from us!"

@app.route('/history-infected-daily', methods=['GET'])
def history_infected_daily():
	dailyDates = {}
	with open(DIR_DATA + "/APIData/history_infected_daily.json", 'r') as FPtr:
		dailyDates = load(FPtr)
	return jsonify(dailyDates)

@app.route('/general', methods=['GET'])
def general():
	generalJSON = {}
	with open(DIR_DATA + "/APIData/index_general.json", 'r') as FPtr:
		generalJSON = load(FPtr)
	return jsonify(generalJSON)

@app.route('/latest-updates', methods=['GET'])
def latest_updates():
	latestUpdatesJSON = {}
	with open(DIR_DATA + "/APIData/latest_updates.json", 'r') as FPtr:
		latestUpdatesJSON = load(FPtr)
	return jsonify(latestUpdatesJSON)

@app.route('/district-values', methods=['GET'])
def district_values():
	districtValuesJSON = {}
	with open(DIR_DATA + "/APIData/district_values.json", 'r') as FPtr:
		districtValuesJSON = load(FPtr)
	return jsonify(districtValuesJSON)

@app.route('/states-affected-numbers', methods=['GET'])
def states_affected_numbers():
	sanJSON = {}
	with open(DIR_DATA + "/APIData/states_affected_numbers.json", 'r') as FPtr:
		sanJSON = load(FPtr)
	return jsonify(sanJSON)

@app.route('/state-date-total-data', methods=['GET'])
def state_date_total_data():
	sdtdJSON = {}
	with open(DIR_DATA + "/APIData/state_date_total_data.json", 'r') as FPtr:
		sdtdJSON = load(FPtr)
	return jsonify(sdtdJSON)

@app.route('/daily-states-complete', methods=['GET'])
def daily_states_complete():
	dscJSON = {}
	with open(DIR_DATA + "/APIData/daily_states_complete.json", 'r') as FPtr:
		dscJSON = load(FPtr)
	return jsonify(dscJSON)

@app.route('/district-date-total-data', methods=['GET'])
def district_date_total_data():
	ddtdJSON = {}
	with open(DIR_DATA + "/APIData/district_date_total_data.json", 'r') as FPtr:
		ddtdJSON = load(FPtr)
	return jsonify(ddtdJSON)

@app.route('/zone-data', methods=['GET'])
def zone_data():
	zdDATA = {}
	with open(DIR_DATA + "/APIData/zone_data.json", 'r') as FPtr:
		zdDATA = load(FPtr)
	return jsonify(zdDATA)

@app.route('/past-twenty-four-hours', methods=['GET'])
def past_twenty_four_hours():
	ptfhDATA = {}
	with open(DIR_DATA + "/APIData/past_twenty_four_hours.json", 'r') as FPtr:
		ptfhDATA = load(FPtr)
	return jsonify(ptfhDATA)

@app.route('/past-two-weeks', methods=['GET'])
def past_two_weeks():
	ptwDATA = {}
	with open(DIR_DATA + "/APIData/past_two_weeks.json", 'r') as FPtr:
		ptwDATA = load(FPtr)
	return jsonify(ptwDATA)

@app.route('/testing-data', methods=['GET'])
def testing_data():
	testingDATA = {}
	with open(DIR_DATA + "/APIData/testing_data.json", 'r') as FPtr:
		testingDATA = load(FPtr)
	return jsonify(testingDATA)

@app.route('/cured-data', methods=['GET'])
def cured_data():
	curedDATA = {}
	with open(DIR_DATA + "/APIData/cured_data.json", 'r') as FPtr:
		curedDATA = load(FPtr)
	return jsonify(curedDATA)

@app.route('/table-data', methods=['GET'])
def table_data():
	# A mix of daily_states_complete and cured_data
	tDATA = {}
	curedDATA = {}
	with open(DIR_DATA + "/APIData/daily_states_complete.json", 'r') as FPtr:
		tDATA = load(FPtr)
	with open(DIR_DATA + "/APIData/cured_data.json", 'r') as FPtr:
		curedDATA = load(FPtr)
	for state in curedDATA:
		try:
			tDATA[state].update(curedDATA[state])
		except:
			# In the random event that curedData has a value that tDATA does not
			tDATA[state] = curedDATA[state]
	return jsonify(tDATA)

@app.route('/csv-historical-state-data', methods=['GET'])
def plot_csv():
	return send_file(DIR_DATA + '/APIData/csv_data.csv', mimetype='text/csv', attachment_filename='csv_data.csv', as_attachment=True)

@app.route('/report-numbers', methods=['GET', 'POST'])
@limiter.limit("1 per 10 seconds")
def report_numbers():
	try:
		if request.method == 'POST':
			formData = {}
			compusloryFields = ['state', 'district', 'infected', 'death', 'number', 'date', 'source']
			optionalFields = ['name']

			for field in compusloryFields:
				if request.form[field] == "":
					return jsonify({"success" : False, "message" : "Could not retrieve " + field})
				formData[field] = escape(request.form[field])

			for field in optionalFields:
				try:
					formData[field] = escape(request.form[field])
				except:
					formData[field] = None

			# The sheet stores data in this formmat:
			# Date, Time, State, District, Infected, Death, Source Link, Name
			submitList = [
				formData['date'],
				datetime.now().strftime("%H:%M"),
				formData['state'],
				formData['district']
			]
			if formData['infected'] in ["True", 'true', True]:
				submitList.append(formData['number'])
				submitList.append(None)
			else:
				submitList.append(None)
				submitList.append(formData['number'])
			submitList.append(formData['source'])
			submitList.append(formData['name'])

			scope = ['https://spreadsheets.google.com/feeds']
			creds = ServiceAccountCredentials.from_json_keyfile_name(DIR_DATA + '/res/crowdsourcing_creds.json',scope)
			client = gspread.authorize(creds)

			with open(DIR_DATA + "/res/crowdsourcing_URL", 'r') as F:
				URL = F.read()
			sheet = client.open_by_url(URL).worksheet('Sheet1')

			sheet.append_row(submitList)

			return jsonify({"success" : True, "message" : "Thank you!"})
		else:
			return jsonify({"success" : False, "message" : "Please post some data"})	
	except Exception as e:
		print (e)
		return jsonify({"success" : False, "message" : str(e)})

@app.route('/i-donated-a-rick-roll', methods=['GET'])
def donated():
	try:
		with open("rick_roll_count.json", 'r') as FPtr:
			rrJSON = load(FPtr)
		rrJSON["rick-rolled"] += 1
		with open("rick_roll_count.json", 'r') as FPtr:
			dump(rrJSON, FPtr)
	except:
		rrJSON = {"rick-rolled" : 1}
		with open("rick_roll_count.json", 'w') as FPtr:
			dump(rrJSON, FPtr)
	finally:
		print ("Rick rolled someone! :yay:")

	return jsonify({"message": "LMAO"})

##### PUBLIC

@app.route('/covindia-history-district-data', methods=['GET'])
def covindia_district_date_data():
	cdddJSON = {}
	with open(DIR_DATA + "/PublicData/covindia_district_date_data.json", 'r') as FPtr:
		cdddJSON = load(FPtr)
	return jsonify(cdddJSON)

@app.route('/covindia-present-state-data', methods=['GET'])
def covindia_state_data():
	csdJSON = {}
	with open(DIR_DATA + "/PublicData/covindia_state_data.json", 'r') as FPtr:
		csdJSON = load(FPtr)
	return jsonify(csdJSON)

@app.route('/covindia-present-general-data', methods=['GET'])
def covindia_general_data():
	cgdJSON = {}
	with open(DIR_DATA + "/PublicData/covindia_general_data.json", 'r') as FPtr:
		cgdJSON = load(FPtr)
	return jsonify(cgdJSON)

@app.route('/covindia-raw-data', methods=['GET'])
def covindia_raw_data():
	crdJSON = {}
	with open(DIR_DATA + "/PublicData/covindia_raw_data.json", 'r') as FPtr:
		crdJSON = load(FPtr)
	return jsonify(crdJSON)

@app.route('/covindia-raw-data-csv', methods=['GET'])
def covindia_raw_data_csv():
	return send_file(DIR_DATA + '/PublicData/covindia_raw_data_csv.csv', mimetype='text/csv', attachment_filename='covindia_raw_data.csv', as_attachment=True)
