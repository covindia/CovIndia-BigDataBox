"""
	`test.py` is the program that is run on Travis CI. Look at .travis.yml
	for the configuration.

	Author: IceCereal
"""

from BigDataBox import minion

if __name__ == "__main__":
	print ("Begin Tests...")

	minion.do_your_work(testing=True)

	print ("Tests Complete!")
