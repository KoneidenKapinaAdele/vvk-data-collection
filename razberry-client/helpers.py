
import sys

logfile = open("sensors.log", "a")

def report_exception():
	e = sys.exc_info()
	print("Unexpected exception:")
	print(e[1])
	print("Backtrace:")
	print(e[2])

def log(*stuff):
	print(stuff)
	for item in stuff: logfile.write(item + '\n')
	logfile.flush()

