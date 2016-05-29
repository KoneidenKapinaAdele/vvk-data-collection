
import config as c
import requests
from requests.auth import HTTPBasicAuth
from secret_config import zway_password

def getsensorvalue(dev):
	name, id, place, type, path = dev
	value = requests.get(c.zway_url + (c.zway_pattern % path),
		auth=HTTPBasicAuth(c.zway_user, zway_password)).json()
	return float(value) if type != 'closed' else 1. - value

def sendsensorvalue(dev, value):
	name, id, place, type, path = dev
	print "%s (%s) is %s" % (name, type, value)
	message = dict(device_id=id, place_id=place, type=type, value=value)
	return requests.post(c.vvk_url, json=message)

def updatedevice(dev):
	return sendsensorvalue(dev, getsensorvalue(dev))

if __name__ == '__main__':
	for device in c.devices: updatedevice(device)

