
import config as c
from secret_config import zway_password
import requests
import time
from requests.auth import HTTPBasicAuth
from readsensors import sendsensorvalue
from helpers import log, report_exception

def get_updates_since(timestamp):
	return requests.get(c.zway_poll_url + str(timestamp),
		auth=HTTPBasicAuth(c.zway_user, zway_password)).json()

def updated_time(response):
	return response["updateTime"]

def devices(response):
	return [(dev, state) for dev, state in response.iteritems()
		if isinstance(state, dict)
		if "val" in state or "level" in state]

def device_level(devstate):
	if "val" in devstate: return devstate['val']['value']
	return devstate['level']['value']

device_map = dict((c.zway_poll_pattern % dev[4][:4], dev) for dev in c.devices)

def devices_mapped(devices):
	return [(device_map[dev], device_level(state))
		for dev, state in devices]

def value_normalise(devinfo, value):
	type = devinfo[3]
	return float(value) if type != 'closed' else 1. - value

def update_all_devices(updates):
	for devinfo, value in devices_mapped(devices(updates)):
		sendsensorvalue(devinfo, value_normalise(devinfo, value))

def update_loop(interval):
	timestamp = 0
	while True:
		log("updates since %d:" % timestamp)
		try:
			updates = get_updates_since(timestamp)
			update_all_devices(updates)
			timestamp = updated_time(updates)
		except: report_exception()
		time.sleep(interval)

if __name__ == '__main__':
	update_loop(1)

