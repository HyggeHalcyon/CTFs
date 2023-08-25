import requests
from bs4 import BeautifulSoup

url = 'http://'
index = '/flag.txt'
cookies = {"sesson" : "randomSHA256"}

data = {
    "data" : "1337"
}

response = requests.post(url + index, data=data, cookies=cookies)
print(response.text)