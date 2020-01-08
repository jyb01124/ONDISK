# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

class script_editor:
    del_slash = ["n", "t"]
    recover_char = ["\\", "/"]
    extract_tag = [["div", "", "player"], ["script", "text/javascript", ""]]
    script_tag = ["<script>", "<script type=\"text/javascript\">", "</script>"]
    deny = ["\\", "?", "*", "\"", "<", ">", "|"]

    def bs(self, script, tag, id="", type=""):
        return BeautifulSoup(str(script), 'html.parser').find_all(tag, id=id, type=type)[0]

    def del_backslash(self, script, del_string):
        change = "\\" + del_string
        return script.replace(change, "")

    def recovery_character(self, script, recovery_string):
        change = "\\" + recovery_string
        return script.replace(change, recovery_string)

    def addQuotes(self, string):
        return '"' + string + '"'

    def script_tag_del(self, script):
        for del_tag in self.script_tag:
            script = script.replace(del_tag, "")
        return script