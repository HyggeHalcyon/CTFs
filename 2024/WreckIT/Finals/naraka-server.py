from flask import Flask, request
import requests
import re

app = Flask(__name__)

SYSTEM_URL = 'http://13.212.152.221:5000/api/flag'
SYSTEM_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNDIwNjIyOSwianRpIjoiNzliNmQwYWMtMDZlNS00NTliLWE4ZjAtMGM5MjYxNjllM2Q4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VybmFtZSI6IkdpcmxzIEJhbmQgQ3J5In0sIm5iZiI6MTcyNDIwNjIyOSwiY3NyZiI6ImRjY2NhZjM3LTgyMDYtNDI1Ny04MThmLTBjZDg3MDgwYTU4NiIsImV4cCI6MTcyNDI5MjYyOX0.hPz00_Z06cWm0VtzpjZgvjdor4n78vzqmTT3ouMsIIM'


@app.route('/', methods=['POST'])
def submit_flag():
    flag = request.form.get('flag')
    flag = re.search(r'WreckIT50\{([^}]+)\}', flag).group(1)
    r = requests.post(
            SYSTEM_URL,
            headers={
                'Authorization': f"Bearer " + SYSTEM_TOKEN,
                'Content-Type': 'application/json'
            },
            json={'flag': flag},
            )
    try:
        print(r.status_code)
        print(r.json())
        return resp
    except:
        return "ERROR"

if __name__ == '__main__':
    app.run(port=5555)