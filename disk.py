import requests, sys, os, struct
from bs4 import BeautifulSoup
import video_image
from email.mime.multipart import MIMEMultipart

headers ={
    "Content-Type" : "application/x-www-form-urlencoded",
    "User-Agent" : "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Host" : "client.ondisk.co.kr",
    "Cache-Control" : "no-cache",
    "Content-Length" : "77"
}

cookies = {
    "Intro_domain_chk" : "client.ondisk.co.kr",
    "charge" : "done",
    "mid" : "9gd2314897aagd2314897abgd2314897acgd2314897adgd2314897a95d2314897a96d2314897a25d2314897ab5d2314897a",
    "UID" : "jsal12345",
    "nick" : "jyb01124",
    "join_path" : "ad",
    "isNameValidation" : "1",
    "Validation_s" : "TQ%3D%3D",
    "Validation_b" : "MTk5MDExMjQ%3D",
    "grade" : "1",
    "credit" : "592%7C%7C122",
    #"ration" : "1578535501%7C1581260400%7C00%7C24%7C6",
    "adult" : "1",
    "cmn_cash" : "157",
    "bns_cash" : "3060",
    "coupon":"39",
    "sch_use" : "Y",
    #"Lidx" : "%241%24r9u4s8kG%24FE.51wztTxYTyvDiVBZhj.",
    "SCkey" : "OWdkMjMxNDg5N2FhZ2QyMzE0ODk3YWJnZDIzMTQ4OTdhY2dkMjMxNDg5N2FkZ2QyMzE0ODk3YTk1ZDIzMTQ4OTdhOTZkMjMxNDg5N2EyNWQyMzE0ODk3YWI1ZDIzMTQ4OTdhfGp5YjAxMTI0fDE%253D"
}

auth_data = {
    "mb_id" : "jsal12345",
    "mb_pw" : "gagaseoro1@",
    "mode" : "login",
    "act" : "ok",
    "secu" : "1",
    "x" : "15",
    "y" : "22",
    "type" : "app"
}

file_data = {
    "code_check" : "N",
    "copyr_code" : "",
    "act" : "ok",
    "user_id" : "jsal12345",
    "code_title" : "�Ϲ�",
    "option_title" : "",
    "new_option" : "|||||",
    "filetype" : "file",
    "uploader" : "",
    "filepath" : "",
    "code_cate" : "ADT",
    "code" : "ADT_001",
    "flag_adult" : "1",
    "cash" : "30",
    "n_alignment" : "",
    "chkPreviewMode" : "",
    "upload_type" : "1",
    "ssomon_update" : "1",
    "K_Kof_id" : "",
    "O_Kof_id" : "jsal12345",
    "link_idx" : ""
    }

header ={
    "Content-Type" : "application/x-www-form-urlencoded",
    "User-Agent" : "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Host" : "client.ondisk.co.kr",
    "Cache-Control" : "no-cache"
    #"Content-Length" : "77"
}

code_title = [37, 99, 48, 37, 99, 102, 37, 98, 57, 37, 100, 100]

url = "http://client.ondisk.co.kr/index.php"

videopath = "C:\\Users\\jyb01\\Desktop"
file_name = "Alice and the Way of Sex [Vincent] [Hentai] -sound edit-.mp4"
filepath = videopath + "\\" + file_name
filesize = str(os.path.getsize(filepath))

V = video_image.video_thumbnail_make()
V.set_file(file_name, videopath)
V.video_init()
V.img_save(V.run(), "pp")

image_name = "pp.jpg"
with requests.Session() as s:
    response = s.post(url, headers=header, cookies=cookies, data=auth_data)
    print(response.status_code)
    
    header["Accept"] = "text\*"
    header["User-Agent"] = "Mozilla/4.0"
    header["Host"] = "uploadbbs.ondisk.co.kr"
    header["Content-Type"] = "multipart/form-data; boundary=---------------------------7d42ce321e03f0"

    files = (
        ("AttachFile",(image_name, open(image_name, "rb"), "image/pjpg")),
        ("act",(None, int.to_bytes(28523, 2, 'big'))),
        ("imageWidth",(None)),
        ("imageHeight",(None)),
        ("alignment",(None)),
        ("h",(None, int.to_bytes(60, 1,'big'))),
        ("b",(None, int.to_bytes(60, 1,'big'))),
        ("v",(None, int.to_bytes(60, 1,'big')))
    )
    
    related = MIMEMultipart('form-data','---------------------------7d42ce321e03f0')

    header = dict(related.items())
    header['User-Agent'] = 'sitename.app'
    header['referer'] = 'http://www.sitename.com'

    files = {
        'app_id':(None, '123123'),
        'id':(None, 'idid'),
        'mode':(None, 'write'),
        'subject':(None, 'subject'),
        'user_id':(None, '456456'),
        'memo_block[0]':(None, 'memoblock')
    }

    url = "http://uploadbbs.ondisk.co.kr/editor/insert_image.php"
    response = s.post(url, headers=header, cookies=cookies, files=files)
    print(response._content)
    crw = str(response._content).split(")")[0].split("(")[1].replace("\\","").replace("'","")
    print(crw)

    image_url = "http://uploadbbs.ondisk.co.kr" + crw

    header['Connection'] = "Keep-Alive"
    header['User-Agent'] = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)"
    
    print(image_url)
    response = s.get(image_url, headers=header, cookies=cookies)
    print(response.status_code)

    url = "http://uploadbbs.ondisk.co.kr/main/module/bbs_uploadPrc.php"
    
    header['Content-Type'] = "application/x-www-form-urlencoded"
    header['Host'] = "uploadbbs.ondisk.co.kr"

    del header['Connection']

    bbs_content = '<P><IMG border=0 alt="" src="'+ image_url +'"></P><P>&nbsp;</P>'
    mmsv = "-1||" + filesize + "||" + filepath
    
    c_title = b''
    for i in code_title:
        c_title += int.to_bytes(i, 1,'big')

    file_data["title"] = file_name
    file_data["contents"] = bbs_content
    file_data["mmsv_files"] = mmsv
    file_data["filename"] = file_name
    file_data["size"] = filesize
    file_data["code_title"] = c_title

    response = s.post(url, headers=header, cookies=cookies, data=file_data)
    print(response._content)




    