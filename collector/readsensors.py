
import config
import requests
from requests.auth import HTTPBasicAuth
from secret_config import zway_password

def getsensorvalue(type, path):
	return requests.get(config.zway_url + (config.zway_pattern % path),
		auth=HTTPBasicAuth(config.zway_user, zway_password)).json()

def reportdevice(dev):
	name, id, place, type, path = dev
	print "%s (%s) is %s" % (name, type, getsensorvalue(type, path))

if __name__ == '__main__':
	for device in config.devices: reportdevice(device)

