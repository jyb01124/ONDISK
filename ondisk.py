import requests, sys
from Naked.toolshed.shell import execute_js, muterun_js

data_login = { 'mb_id' : 'jsal12345',
         'mb_pw' : 'gagaseoro1@',
         'mode' : 'login',         
         'act' : 'ok',
         'secu' : '1', 
         'x' : '15',
         'y' : '22',
         'type' : 'app' }

headers_login = { 'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)', 
                'Host' : 'client.ondisk.co.kr',
                'Content-Length' : '77',
                'Cache-Control' : 'no-cache'}

cookies_login = {'Intro_domain_chk': 'client.ondisk.co.kr'}

data_bbs = { "code_check" : "N",
             "copyr_code" : "",
             "act" : "ok",
             "size" : "25979792",
             "user_id" : "jsal12345",
             "code_title" : "TeamViewer",
             "option_title" : "",
             "new_option" : "|||||",
             "filename" : "TeamViewer_Setup.exe",
             "filetype" : "file",
             "mmsv_files" : "-1||25979792||C:\\Users\\jyb01\\Downloads\\TeamViewer_Setup.exe",
             "contents" : "<P>TeamViewer_Setup.exe<IMG border=0 alt=\"\" src=\"http://uploadbbs.ondisk.co.kr/temp/contents/2200829_RCFJ_1572525185.jpg\"></P><P>&nbsp;</P>",
             "uploader" : "",
             "title" : "TeamViewer_Setup.exe",
             "filepath" : "C:\\Users\\jyb01\\Downloads\\TeamViewer_Setup.exe",
             "code_cate" : "UTL",
             "code" : "UTL_010",
             "flag_adult" : "0",
             "cash" : "10",
             "n_alignment" : "",
             "chkPreviewMode" : "",
             "upload_type" : "1",
             "ssomon_update" : "1",
             "K_Kof_id" : "",
             "O_Kof_id" : "jsal12345",
             "link_idx" : "" }

headers_bbs = { 'Content-Type' : 'application/x-www-form-urlencoded',
                'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
                'Host' : 'uploadbbs.ondisk.co.kr',
                'Content-Length' : '679',
                'Cache-Control' : 'no-cache' }

cookies_bbs = {  'Intro_domain_chk':'client.ondisk.co.kr',
                 'charge':'done',
                 'mid':'9gd2314897aagd2314897abgd2314897acgd2314897adgd2314897a95d2314897a96d2314897a25d2314897ab5d2314897a',
                 'UID':'jsal12345',
                 'nick':'jyb01124',
                 'join_path':'ad',
                 'isNameValidation':'1',
                 'Validation_s':'TQ%3D%3D',
                 'Validation_b':'MTk5MDExMjQ%3D',
                 'grade':'1',
                 'ration':'1570413901%7C1573138800%7C00%7C24%7C6',
                 'credit':'592%7C%7C122',
                 'adult':'1',
                 'cmn_cash':'757',
                 'bns_cash':'1120',
                 'coupon':'32',
                 'sch_use':'Y',
                 'Lidx':'%241%24WPY5VsC5%24lWf4NTmVnROFKGvjGPBbV.',
                 'SCkey':'OWdkMjMxNDg5N2FhZ2QyMzE0ODk3YWJnZDIzMTQ4OTdhY2dkMjMxNDg5N2FkZ2QyMzE0ODk3YTk1ZDIzMTQ4OTdhOTZkMjMxNDg5N2EyNWQyMzE0ODk3YWI1ZDIzMTQ4OTdhfGp5YjAxMTI0fDE%253D' }

with requests.Session() as s:
    #program_start = s.post('http://uploadbbs.ondisk.co.kr/main/module/bbs_uploadPrc.php', data=data_bbs, headers=headers_bbs, cookies=cookies_bbs)
    #print(program_start.status_code)
    #print(program_start.cookies.keys())
    #print(program_start.text)
    f = open("./ondisk.html", 'w')
    f.write(str(program_start.text))
    f.close()
    program_start = s.post('http://C:/Users/jyb01/Desktop/ondisk.html', headers=headers_bbs, cookies=cookies_bbs)
