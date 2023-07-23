import requests
from bs4 import BeautifulSoup

url = 'https://hi.tjc.tf'
index = '/secret-b888c3f2.svg'

response = requests.get(url + index)
print(response.text[276:305])