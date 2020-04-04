import flask
from flask import jsonify, request, escape
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
	key_func=get_remote_address,
	default_limits=["1 per 1 second"]
)

@app.route('/', methods=['GET'])
def home():
	return "<a href=\"https://covindia.com\">Click here to go to https://covindia.com</a>. You were not supposed to stumble here.<br><br>But now that you did, hello from us!"

@app.route('/daily-dates', methods=['GET'])
def daily_dates():
	dailyDates = {}
	with open(DIR_DATA + "/APIData/daily_dates.json", 'r') as FPtr:
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
