
import config
import requests
import time
import json
from random import randint
import threading
from scipy.stats import norm

def sleep(secs):
    print("sleeping", secs)
    time.sleep(secs)

def daytime_as_float():
    t = time.localtime()
    return t.tm_hour + t.tm_min / 60. + t.tm_sec / 3600.

def occu_probability_calculator(peaks, stddev):
    distributions = [norm(loc=peak, scale=stddev) for peak in peaks]
    return lambda moment: sum(d.pdf(moment) for d in distributions)

def data_gen(device, prob_fn):
    place, device = device
    while True:
        prob = prob_fn(daytime_as_float())
        print("current probability of being occupied is", prob)
        perform_time = randint(30,300)
        # prob = pt / (pt+it) <=> it = pt/prob - pt
        idle_time = perform_time / prob - perform_time
        yield dict(place_id=place, device_id=device, type="movement", value=1)
        sleep(perform_time)
        yield dict(place_id=place, device_id=device, type="movement", value=0)
        sleep(min(idle_time, 3600))

def send_data_from_generator(url, data_generator):
    for event in data_generator:
        print(event)
        r = requests.post(url, data=json.dumps(event),
                headers={'content-type': 'application/json'})

def start_thread(function, args):
    t = threading.Thread(target=function, args=args)
    t.start()
    return t

if __name__ == '__main__':
    for device in config.devices:
        start_thread(send_data_from_generator,
                (config.back_url + config.event_endpoint,
                    data_gen(device,
                        occu_probability_calculator(config.rush_hours,
                            config.deviation))))

