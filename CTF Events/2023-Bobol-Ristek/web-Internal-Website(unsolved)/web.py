import requests
from bs4 import BeautifulSoup

url = 'http://13.229.76.35:9011/'

#reference: 


data = {
    "read" : payload
}

response = requests.post(url, data=data)
print(response.text)