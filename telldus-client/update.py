
import sys, requests, json

from config import event_post_url
from query_telldus import devices, new_events, convert_event, latest_timestamp
from time import sleep, localtime
from requests.exceptions import RequestException
from traceback import print_tb

def send_event(event):
    print("%s %s is %s at %s" %
            (event['type'], event['place_id'], event['value'], event['time']))
    try: return requests.post(event_post_url, data=json.dumps(event),
		headers={'Content-type': 'application/json'}, timeout=10)
    except RequestException as e: log("Post problem:", e)

def fetch_and_send(since):
    events = new_events(devices(), since)
    for event in events:
        response = send_event(convert_event(event))
        print("%d: %s" % (response.status_code, response.text))
	if response.status_code != 201:
		raise RequestException("No event created")
    return latest_timestamp(events, since)

def update_loop(interval, since=0):
    while True:
        print("updates since %d (at %02d:%02d):" %
			(since, localtime().tm_hour, localtime().tm_min))
        try: since = fetch_and_send(since)
        except:
		print(sys.exc_info())
		print_tb(sys.exc_info()[2])
        sleep(interval)

if __name__ == '__main__':
    update_loop(10, 1466085093)

