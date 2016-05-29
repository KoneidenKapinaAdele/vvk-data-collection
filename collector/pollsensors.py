
import config as c
from secret_config import zway_password
import requests
from requests.auth import HTTPBasicAuth
from readsensors import sendsensorvalue

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

if __name__ == '__main__':
	update_all_devices(get_updates_since(1464531287))

