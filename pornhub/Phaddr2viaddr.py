# -*- coding: utf-8 -*-
import requests, time, queue
from bs4 import BeautifulSoup
from Script_editor import script_editor

class phaddr2viaddr:
    def __init__(self):
        super().__init__()
        self.editor_tools = script_editor()

    def connect(self, url):
        html = requests.get(url).content
        return html

    def Bool2Str(self, content, string):
        one = self.editor_tools.addQuotes(string)
        content = content.replace(string, one)
        two = self.editor_tools.addQuotes(one)
        content = content.replace(two, one)
        return content

    def extract_var(self, content):
        for option in self.editor_tools.extract_tag:
            content = str(self.editor_tools.bs(content, option[0], type=option[1], id=option[2]))
        for char in self.editor_tools.del_slash:
            content = self.editor_tools.del_backslash(content, char)

        content = self.editor_tools.script_tag_del(content)

        for char in self.editor_tools.recover_char:
            content = self.editor_tools.recovery_character(content, char)

        content = self.Bool2Str(content, 'true')
        content = self.Bool2Str(content, 'false')

        return content.split(";")[:-1]

    def make_title(self, header):
        header = eval(str(header[header.find("{"):]))
        return header['video_title']

    def title_check(self, title):
        for d in self.editor_tools.deny:
            if d in title:
                title = title.replace(d, "")
        return title

    def Var2DictObj(self, var_str):
        var_str = var_str.replace("var ", "")
        piece = var_str.split("=")
        piece_cnt = len(piece)
        key = piece[0].replace(" ", "")
        #print(piece)
        if piece_cnt < 2:
            return key, ""
        elif piece_cnt == 2:
            value = piece[1]
        else:
            value = ""
            for cnt in range(1, piece_cnt):
                value += (piece[cnt] + "=")
            value = value[:-1]

        value = value.replace(" ", "").replace('"+"', '').replace("\"", "")

        return key, value

    def var_classific(self, pieces):
        Q = {}
        A = {}
        for i in pieces:
            key, val = self.Var2DictObj(i)
            if (val == "") or ("flashvars" in key) or ("qualityItems" in key) or ("player_mp4_seek" in key) or (
                    "playerObjList" in key) or ("media_" in key):
                continue
            if ("quality_" in key):
                key = int(key.replace("quality_", "").replace("p", ""))
                Q[key] = val
                continue
            A[key] = val
        return Q, A

    def Question(self, Q):
        key = max(Q.keys())
        ws = Q[key].split("/*")
        Q_str = ws[0]
        for string in ws[1:]:
            Q_str += string.split("*/")[1]
        return Q_str

    def puzzle_game(self, Q, A):
        url = ""
        ws = Q.split("+")
        for piece in ws:
            url += A[piece]
        return url

if __name__ == "__main__":
    a = phaddr2viaddr()
    HTML = a.connect("https://www.pornhub.com/view_video.php?viewkey=ph5c52110e6fba6")
    header = a.extract_var(HTML)
    title = a.title_check(a.make_title(header[0]))
    Q, A = a.var_classific(header[1:])
    Q = a.Question(Q)
    url = a.puzzle_game(Q, A)
    print(url)