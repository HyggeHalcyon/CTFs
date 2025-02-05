from flask import Flask, request, jsonify
import requests
import base58


app = Flask(__name__)


TARGET_URL = "http://10.1.2.234/api/login"


@app.route("/proxy/login", methods=["POST"])
def proxy_request():
    data = request.get_json()
    request_data = {
        "username": base58.b58encode(data["username"].encode()).decode(),
        "password": base58.b58encode(data["password"].encode()).decode()
    }
    response = requests.post(TARGET_URL, json=request_data)
    print(response.text)
    return response.text, response.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8181, debug=True)