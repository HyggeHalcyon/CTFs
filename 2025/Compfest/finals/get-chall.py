import requests

baseURL = 'https://api.ctf-compfest.com'
auth_res = requests.post(
    baseURL + "/api/v2/authenticate",
    json={
        "email": "akuazril12@gmail.com",
        "password": "616ee8fd94830cb161ab1906e7e3731a",
    },
    verify=False,
)
jwt = auth_res.json().get("data")

chall_id = 16
res = requests.get(baseURL + f"/api/v2/challenges/{chall_id}/services/", headers={
    "Authorization": "Bearer " + jwt,
}, verify=False)

print(res.json())