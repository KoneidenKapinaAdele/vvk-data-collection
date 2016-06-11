
from requests import post
from json import load, dumps
import sys

for record in load(open(sys.argv[2], "r")):
    if "id" in record: del record["id"]
    post(sys.argv[1], data=dumps(record),
            headers={'content-type': 'application/json'})

