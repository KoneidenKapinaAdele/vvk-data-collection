
import config as c
import requests
from time import sleep
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException
from secret_config import zway_password
from helpers import log, report_exception

def getsensorvalue(dev):
	name, id, place, type, path = dev
	value = requests.get(c.zway_url + (c.zway_pattern % path),
		auth=HTTPBasicAuth(c.zway_user, zway_password)).json()
	return float(value) if type != 'closed' else 1. - value

def sendsensorvalue(dev, value):
	name, id, place, type, path = dev
	log("%s (%s) is %s" % (name, type, value))
	message = dict(device_id=id, place_id=place, type=type, value=value)
	try: return requests.post(c.vvk_url, json=message)
	except RequestException as e: log("Post problem:", e)

def updatedevice(dev):
	return sendsensorvalue(dev, getsensorvalue(dev))

def updateloop(interval):
	import sys
	while True:
		try:
			for device in c.devices: updatedevice(device)
		except: report_exception()
		sleep(interval)

if __name__ == '__main__':
	updateloop(10)

