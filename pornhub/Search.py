# -*- coding: utf-8 -*-
import requests, time
from bs4 import BeautifulSoup
from Script_editor import script_editor

class search:
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ko,ko-KR;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.pornhub.com",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
    }

    cookies = {
        "platform_cookie_reset": "pc",
        "platform": "pc",
        "RNLBSERVERID": "ded6889",
        "SMPop_0": "1578276188894",
        "ua": "237aa6249591b6a7ad6962bc73492c77",
        "bs": "61ixd7erb1t093eelyvkqwxm2tjknjlf",
        "ss": "285712445419885464",
        "_ga": "GA1.2.1296553486.1578275327",
        "_gid": "GA1.2.1782756753.1578275327",
        "_gat": "1"
    }

    var = {
        "class": "js-pop videoblock videoBox",
        "data-segment": "straight",
        "data-entrycode": "VidPg-premVid",
        "data-id": True,
        "id": True,
        "_vkey": True
    }

    v_url = "https://www.pornhub.com/view_video.php?viewkey="
    search_page = "https://www.pornhub.com/video/search?search="

    del_slash = ["n", "t"]
    recover_char = ["\\", "/"]

    def __init__(self):
        super().__init__()
        self.editor_tools = script_editor()
        self.search_url = ""
        self.R = None

    def set_word(self, word):
        self.search_word = word

    def make_url(self, page):
        self.search_url = self.search_page + self.search_word.replace(" ", "%20") + "&" + "page=" + str(page)

    def connect(self):
        self.R = requests.get(self.search_url)
        if int(self.R.status_code / 100) == 4:
            return True
        return False

    def extract_li_tag_list(self):
        html = str(self.R.content)
        for char in self.editor_tools.del_slash:
            html = self.editor_tools.del_backslash(html, char)
        for char in self.editor_tools.recover_char:
            html = self.editor_tools.recovery_character(html, char)
        for char in self.editor_tools.recover_char:
            html = self.editor_tools.recovery_character(html, char)

        return BeautifulSoup(str(html), 'html.parser').find_all("li", attrs=self.var)

    def extract_info(self, li_tag_list):
        return_addr = []
        for cur_li in li_tag_list:
            li_tag = BeautifulSoup(str(cur_li), 'html.parser')
            img_tag = li_tag.img.extract()
            try:
                img_tag["data-image"]
            except:
                return_addr.append(self.v_url + li_tag.li['_vkey'])
                #img_tag['data-src']
                #img_tag['data-mediabook']
        return return_addr