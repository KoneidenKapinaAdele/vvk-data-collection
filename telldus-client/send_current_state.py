
from apicall import request

def device_list(): return request('devices/list')

def devices(json): return [int(dev['id']) for dev in json['device']]

types = {'liike': 'movement', 'ovi': 'closed'}

if __name__ == '__main__':
    print devices(device_list())

