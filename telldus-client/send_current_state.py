
import sys

from apicall import request
from datetime import datetime
from time import time

def device_list(): return request('devices/list')

def devices(json):
    return [(int(dev['id']), dev['name'])
            for dev in json['device'] if dev['online']]

def device_events(dev_id, since):
    return request('device/history',
            {'id': dev_id, 'from': since, 'to': time()})

def event_enrich(event, dev_id, name):
    res = event.copy()
    res['id'] = dev_id
    res['name'] = name
    return res

def new_events(devices, since):
    return [event_enrich(event, dev_id, name)
            for dev_id, name in devices
            for event in device_events(dev_id, since)['history']]

def latest_timestamp(events, since):
    return max(since, max(int(event['ts']) for event in events))

types = {'liike': 'movement', 'ovi': 'closed'}

if __name__ == '__main__':
    since = int(sys.argv[1])
    events = new_events(devices(device_list()), since)
    print(events, latest_timestamp(events, since))

