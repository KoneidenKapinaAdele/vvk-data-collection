
import sys

from apicall import request
from datetime import datetime
from time import time

def device_list(): return request('devices/list')

def devices():
    return [(int(dev['id']), dev['name'])
            for dev in device_list()['device']] # if dev['online']]

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
    return max([since] + [int(event['ts']) + 1 for event in events])

def ts_to_iso(ts):
    return datetime.fromtimestamp(ts).isoformat()

types = {'liike': 'movement', 'ovi': 'closed'}

def convert_event(event):
    name = event['name'].split()
    dev_type = types.get(name[0], 'none')
    dev_place = int(name[1])
    state = int(event['state'])
    value = 2 - state if dev_type == 'closed' else state - 1
    return dict(device_id=event['id'], place_id=dev_place, type=dev_type,
            time=ts_to_iso(event['ts']), value=value)

if __name__ == '__main__':
    since = int(sys.argv[1])
    events = new_events(devices(), since)
    print([convert_event(ev) for ev in events], latest_timestamp(events, since))

