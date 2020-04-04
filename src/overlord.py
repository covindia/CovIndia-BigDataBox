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
# TODO: Add verbosity

# TODO: Complete todos

args = parser.parse_args()

DIR_RES = "res/"
DIR_PRODUCTION = "live/"
DIR_SRC = "src/"

DIR_DATA = "../data/"

overallCount = 0

if __name__ == "__main__":
	minutes = args.minutes[0]

	# These are if the scrapbois are editing the sheet and we get some sort of incomplete data
	# A race condition between a computer thread and human fingers
	ERROR_THRESHOLD = 5
	error_count = 0

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

	while (error_count < ERROR_THRESHOLD):
		try:
			# Make minion run and do our dirty work
			minion.do_your_work() # I know, cute right?
			error_count = 0

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


		except Exception as e:
			print (e)
			error_count += 1

			pigeonCarrierMessage = {
				"text": "Encountered a glitch. Will try again in " + str(minutes) + " minutes. Attempt (" + str(error_count) + "/" + str(ERROR_THRESHOLD) + ")",
				"attachments": [ { "text": "Exception: " + str(e) } ]
			}

			response = requests.post(
				slackCredentials["payloadURL"], json=pigeonCarrierMessage, headers={'Content-Type': 'application/json'}
			)

			if response.status_code != 200:
				print ("I failed my mission of delivering the message: Encoutered a glitch. ERROR: " + response.text)

		count += 1
		sleep (60*minutes)

	# Okay.... so the while loop exited. Not a good sign

	# Overlord-Bodyguard will sweep in and report it to the Cereal God on slack
	pigeonCarrierMessage = {
		"text": "<@" + slackCredentials["cerealGodUserID"] + ">! IMPORTANT: Overlord has been compromised! Manual restart required",
	}

	response = requests.post(
		slackCredentials["payloadURL"], json=pigeonCarrierMessage, headers={'Content-Type': 'application/json'}
	)

	if response.status_code != 200:
		raise ValueError("I failed my mission of delivering the message that overlord has been compromised. ERROR: " + response.text)
	else:
		print ("\n\nIceCereal has been notified\n\n")



"""
	Note from the Cereal God himself (Omagosh! *froth forms*):
		Having fun with code / comments is important.

		That being said, don't take my notes seriously. I'm a plebian who uses debian.

"""