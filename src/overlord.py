"""
	This is the master program that takes care of everything. It summons other programs and does the necessary
	things required to keep https://covindia.com running.

	Overlord does a lot of work, indeed. What must be it's motivation, you ask? It's this stackoverflow answer:
	https://stackoverflow.com/a/1732454

	Have fun going down that hole.

	Author: IceCereal
"""

from subprocess import run
from datetime import datetime
from time import sleep
import requests
from BigDataBox import minion
from json import load, dump, dumps
from argparse import ArgumentParser

parser = ArgumentParser(description="https://covindia.com's complete overlord. Warning: Can be slightly moody  once in a while")
parser.add_argument("--minutes", '-m', type=int, nargs=1, required=False, default=[5], help="amount of time (in minutes, duh) to sleep for between updates of the website")

# TODO: Add arguments for RES, PUBLISH, SRC _DIRS
# TODO: Add arguments for branch
# TODO: Add verbosity

# TODO: Complete todos

args = parser.parse_args()

DIR_RES = "res/"
DIR_PRODUCTION = "live/"
DIR_SRC = "src/"

DIR_DATA = "../data/"

overallCount = 0

if __name__ == "__main__":
	# Set our working variables
	minutes = args.minutes[0]
	count = 1
	countStopper = int((60 / minutes)/2)

	with open(DIR_RES + "slack_resources.json", 'r') as FPtr:
		slackCredentials = load(FPtr)

	# Overlord-Bodyguard: Reporting for duty
	pigeonCarrierMessage = {
		"text": "Report:",
		"attachments": [ { "text": "Going online, setting the crows on watch."} ]
	}

	response = requests.post(
		slackCredentials["payloadURL"], json=pigeonCarrierMessage, headers={'Content-Type': 'application/json'}
	)

	if response.status_code != 200:
		print ("I failed my mission of delivering the message: Going online. ERROR: " + response.text)

	try:
		overallCount += 1
		while True:
			# Check if our code has changed from the git repository
			# run(['git', 'fetch'])
			# run(['git', 'pull', 'origin', branch])

			# Make minion run and do our dirty work
			minion.do_your_work() # I know, cute right?

			# Data needs to be distributed amongst droplets. Triggers through git hooks
			run('git add .'.split(), cwd=DIR_DATA)
			run(['git', 'commit', '-a', '-m', '"Update ' + datetime.now().strftime("%Y-%m-%d %H:%M")+'"'], cwd=DIR_DATA)

			run(['git', 'push'], cwd=DIR_DATA)

			print ("Sleeping...")
			if count >= countStopper:
				count = 1
				# Overlord-Bodyguard: Reporting for duty
				pigeonCarrierMessage = {
					"text": "Report:",
					"attachments": [ { "text": "Update: Overlord is Alive."} ]
				}

				response = requests.post(
					slackCredentials["payloadURL"], json=pigeonCarrierMessage, headers={'Content-Type': 'application/json'}
				)

				if response.status_code != 200:
					print ("I failed my mission of delivering the message: Hourly Update. ERROR: " + response.text)

			count += 1
			overallCount = 0
			sleep (60*minutes)

		mainFn()

	except Exception as e:

		print (e)

		# Overlord-Bodyguard will sweep in and report it to the Cereal God on slack
		pigeonCarrierMessage = {
			"text": "<@" + slackCredentials["cerealGodUserID"] + ">! IMPORTANT: Overlord has been compromised. Treat this as urgent priority!",
			"attachments": [ { "text": "Exception: " + str(e) } ]
		}

		response = requests.post(
			slackCredentials["payloadURL"], json=pigeonCarrierMessage, headers={'Content-Type': 'application/json'}
		)

		if response.status_code != 200:
			raise ValueError("I failed my mission of delivering the message that overlord has been compromised. ERROR: " + response.text)
		else:
			print ("Cereal God Has been notified. We must await his action.")

