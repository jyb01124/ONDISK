from bs4 import BeautifulSoup
import requests

def del_remark(String):
    total = ""
    open_remark = String.split("/*")
    del open_remark[0]
    for STR in open_remark:
        close_remark = STR.split("*/")
        if len(close_remark) <= 1:
            continue
        total += close_remark[1]
    url_key_list = total.split(" + ")
    return url_key_list

def puzzle_jigsow(puzzle_str, puzzle_key):
    url = ""
    for puzzle in puzzle_str:
        url += puzzle_key[puzzle]
    return url

url = "https://www.pornhub.com/view_video.php?viewkey=ph5d2d1e2ff1e61"
while True:
    url = input("주소 : ")

    html = requests.get(url)
    html = html.content
    secure = {}
    video_url = {}
    switch = False

    soup = BeautifulSoup(str(html),'html.parser')
    a = soup.find_all("div", id="player")

    a = str(a[0]).replace("\\n","")
    a = str(a).replace("\\t","")

    a = str(a).replace('\\"','"')
    a = str(a).replace("\\'","'")
    a = str(a).replace('\\\/','/')

    a = str(a).replace("var ","")

    b = str(a).split(";")

    for i in range(1,len(b)-1):
        
        tmp = b[i].split("=")
        LEN = len(tmp)

        if LEN > 2:
            for j in range(2,LEN):
                tmp[1] = tmp[1] + "=" + tmp[j]

        try:
            tmp[1] = tmp[1].replace('" + "',"")
            tmp[1] = tmp[1].replace('"',"")
        except:
            continue

        if '</scripts>' in tmp[0]:
            break

        salt_list = ['media', 'flashvars', 'player_mp4_seek']

        for salt in salt_list:
            if salt in tmp[0]:
                switch = True
        
        if switch == True:
            switch = False
            continue

        if 'quality_' in tmp[0]:
            video_url[tmp[0]] = tmp[1]
            continue

        secure[tmp[0]] = tmp[1]

    for key in video_url.keys():
        url_puzzle = del_remark(str(video_url[key]))
        URL = puzzle_jigsow(url_puzzle, secure)

        print(str(key) + " : " + URL)