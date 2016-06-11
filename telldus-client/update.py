
import sys, requests

from config import event_post_url
from query_telldus import devices, new_events, convert_event, latest_timestamp
from time import sleep
from requests.exceptions import RequestException

def send_event(event):
    print("%s %s is %s at %s" %
            (event['type'], event['place_id'], event['value'], event['time']))
    try: return requests.post(event_post_url, json=event)
    except RequestException as e: log("Post problem:", e)

def fetch_and_send(since):
    events = new_events(devices(), since)
    for event in events:
        response = send_event(convert_event(event))
        print("%d: %s" % (response.status_code, response.text))
    return latest_timestamp(events, since)

def update_loop(interval, since=0):
    while True:
        print("updates since %d:" % since)
        try: since = fetch_and_send(since)
        except: print(sys.exc_info())
        sleep(interval)

if __name__ == '__main__':
    update_loop(10, 1465576823)

