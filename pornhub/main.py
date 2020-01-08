from Search import search
from Phaddr2viaddr import phaddr2viaddr
from Video_download import video_download
import time

# create object
S = search()
P = phaddr2viaddr()
V = video_download()

page_num = 1
index = 0

errlog_file = open("errlog.txt","w")
suclog_file = open("suclog.txt","w")

try:
    while True:
        # search word
        S.set_word("fuck")
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
                V.set_param(P.puzzle_game(Q, A))
                
                if V.url_confirm(TITLE) == 1:
                    print("main : Connection error")
                    time.sleep(5)
                    err += 1
                    continue
                break
            if err_cnt == 5:
                errlog_file.write("Connection error : " + TITLE + " : " + No + "\n")
                err_cnt = 0
                continue
            print("main : Download Start")
            V.set_filename(TITLE + "." + V.set_file_extension())
            V.file_down()
            print("main : Download End")
            suclog_file.write(TITLE + " : " + str(V.file_length) + ", vKey : " + No.split("viewkey=")[1] + "\n")
            index += 1
        index = 0
        page += 1

except:
    print("page num : ", page_num)
    print("index : ", index)


        

        

        

    






