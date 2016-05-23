
import config
import requests
import time
from random import randint
import threading

def start_thread(function, args):
    t = threading.Thread(target=function, args=args)
    t.start()
    return t

def data_gen(device, peaks, stddev):
    place, device = device
    while True:
        yield dict(place_id=place, device_id=device, type="movement", value=1)
        time.sleep(randint(15,30))

def send_data_from_generator(url, data_generator):
    for event in data_generator:
        #requests.post(url, json=event)
        print(url, event)

if __name__ == '__main__':
    for device in config.devices:
        start_thread(send_data_from_generator,
                (config.back_url + config.event_endpoint,
                    data_gen(device, config.rush_hours, config.deviation)))

