
import config
import requests
import time
from random import randint
import threading
from scipy.stats import norm

def sleep(secs):
    print("sleeping", secs)
    time.sleep(secs)

def daytime_as_float():
    t = time.localtime()
    return t.tm_hour + t.tm_min / 60. + t.tm_sec / 3600.

def data_gen(device, peaks, stddev):
    place, device = device
    distributions = [norm(loc=peak, scale=stddev) for peak in peaks]
    while True:
        prob = sum(d.pdf(daytime_as_float()) for d in distributions)
        print("current movement probability is", prob)
        perform_time = randint(30,300)
        idle_time = perform_time / prob
        yield dict(place_id=place, device_id=device, type="movement", value=1)
        sleep(perform_time)
        yield dict(place_id=place, device_id=device, type="movement", value=0)
        sleep(min(idle_time, 3600))

def send_data_from_generator(url, data_generator):
    for event in data_generator:
        print(url, event)
        #requests.post(url, json=event)

def start_thread(function, args):
    t = threading.Thread(target=function, args=args)
    t.start()
    return t

if __name__ == '__main__':
    for device in config.devices:
        start_thread(send_data_from_generator,
                (config.back_url + config.event_endpoint,
                    data_gen(device, config.rush_hours, config.deviation)))

