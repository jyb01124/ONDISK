from Search import search
from Phaddr2viaddr import phaddr2viaddr
from Video_download import video_download
import time, datetime, os

import smtplib
from email.mime.text import MIMEText

# create object
S = search()
P = phaddr2viaddr()
V = video_download()

TITLE = ""
No = ""

t = datetime.datetime.today()
log_time = t.strftime('%Y-%m-%d,%H-%M-%S')

page_num = 1
index = 0
word = "orgasm"

PP = ["video", "log", "log/suc", "log/err"]
for path in PP:
    try:
        os.mkdir(path)
    except FileExistsError:
        pass   

EE = "./log/err/errlog-" + log_time + ".txt" 
SS = "./log/suc/suclog-" + log_time + ".txt" 

errlog_file = open(EE,"w")
suclog_file = open(SS,"w")

try:
    suc_list = open("./log/suc_list.txt", "r")
except FileNotFoundError:
    suc_list = open("./log/suc_list.txt", "w")
    suc_list.close()
    suc_list = open("./log/suc_list.txt", "r")

v_url = "https://www.pornhub.com/view_video.php?viewkey="
suc_v_key_list = [] 
suc_L = suc_list.readlines()

cnt = 0
for data in suc_L:
    if cnt == 0:
        cnt += 1
        continue
    suc_v_key_list.append(v_url+str(data).split(",")[2].replace("\n",""))

errlog_file.write(word + "\n")
suclog_file.write(word + "\n")

try:
    while True:
        S.set_word(word)
        S.make_url(page_num)

        if S.connect():
            print("main : 연결 에러")
            time.sleep(5)
            print("main : 연결 재시도.")
            continue
                    
        print("main : 연결 성공")
        HTML_CODE = S.extract_li_tag_list()
        RETURN_ADDR_LIST = S.extract_info(HTML_CODE)

        print("main : 추출 개수 확인")
        if len(RETURN_ADDR_LIST) != 20:
            print("main : 추출 실패")

        for U in RETURN_ADDR_LIST:
            for UU in suc_v_key_list:
                if U == UU:
                    print(U)
                    RETURN_ADDR_LIST.remove(UU)
                    break

        err_cnt = 0
        for No in RETURN_ADDR_LIST:
            HEADER = P.extract_var(P.connect(No))
            TITLE = P.title_check(P.make_title(HEADER[0]))
            Q, A = P.var_classific(HEADER[1:])
            Q = P.Question(Q)
            while True:
                if err_cnt == 5:
                    break
                print("main : " + str(index+1)+"번째")
                print("main : " + TITLE)
                rtn_url = str(P.puzzle_game(Q, A))
                rtn_url = P.chk_url(rtn_url)
                print("main : " + str(rtn_url))
                #rtn_url = str(P.puzzle_game(Q, A))
                V.set_param(rtn_url)
                    
                if V.url_confirm(TITLE) == 1:
                    print("main : Connection error")
                    time.sleep(5)
                    err_cnt += 1
                    continue
                break
            if err_cnt == 5:
                errlog_file.write("Connection error : " + TITLE + " : " + No + "\n")
                err_cnt = 0
                continue
            print("main : Download Start")
            time.sleep(2)
            V.file_down()
            print("main : Download End")
            suclog_file.write(TITLE + "," + str(V.file_length) + "," + No.split("viewkey=")[1] + "\n")
            index += 1
        index = 0
        page_num += 1

except Exception as e:
    sg = smtplib.SMTP('smtp.gmail.com', 587)
    sg.starttls()
    sg.login('kurtz01124@gmail.com', 'pmmamefdgamkmfip')
    err_sub = "FAIL : error : " + TITLE + " : " + No + "\n"
    msg_con = str(e) + "\n"
    print("err msg : " + msg_con)
    print(e.args)
    errlog_file.write(err_sub)
    errlog_file.write(msg_con)

    msg = MIMEText(msg_con)
    msg['Subject'] = err_sub
    sg.sendmail("kurtz01124@gmail.com", "kurtz01124@gmail.com", msg.as_string())
    sg.quit()

    suclog_file.close()
    read_ = open(SS,"r")
    suc_list = open("./log/suc_list.txt", "a")
    R = read_.readlines
    for i in R:
        suc_list.write(str(i))
    read_.close()
    suc_list.close()

errlog_file.close()
suclog_file.close()



        

        

        

    






