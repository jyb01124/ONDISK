from bs4 import BeautifulSoup
import requests
from hyper.contrib import HTTP20Adapter, HTTPAdapter

#https://hitomi.la/search.html?korean


url = "https://hitomi.la/search.html?korean#1"
url = "https://ltn.hitomi.la/galleriesindex/galleries.1577049156.data"

s = requests.Session()
s.mount("https://ltn.hitomi.la", HTTP20Adapter())
r = s.get(url)
print(r.status_code)
if r.status_code == 200:
    html = r._content
    print(str(html).replace("\\n",""))


#html = requests.get(url)
#html = html.content

#soup = BeautifulSoup(str(html),'html.parser')
#print(soup)
#a = soup.find_all("div", id="player")