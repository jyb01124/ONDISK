import common
import requests, zipfile, os
from hyper.contrib import HTTP20Adapter, HTTPAdapter

class hitomi:
    galleryid = ""
    https = "https:"

    header = {
        "accept": "image/webp,image/apng,image/*,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "ko,ko-KR;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
    }

    cookie = {
        "494668b4c0ef4d25bda4e75c27de2817" : "9834942c-6a33-4dbc-b65b-8fd73f1f89c0"
    }

    def input_data(self, gal_num, zipfilename):
        self.galleryid = str(gal_num)
        self.img_list_url = "https://ltn.hitomi.la/galleries/"+ str(self.galleryid) +".js"
        self.header["referer"] = "https://hitomi.la/reader/"+ self.galleryid +".html"
        self.zipfilename = zipfilename

    def galleryinfo_download(self):
        response = requests.get(self.img_list_url)
        txt = response.content.decode('utf-8')

        objts = txt.split("},{")
        objts[0] = objts[0].split("[{")[1]
        objts[len(objts)-1] = objts[len(objts)-1].replace("}]","")

        galleryinfo = []

        for obj in objts:
            tmp_dic = {}
            tmps = obj.split(",")
            for tmp in tmps:
                tmp = tmp.replace('"','')
                tmp = tmp.replace("'","")
                dict_split=tmp.split(":")
                tmp_dic[dict_split[0]] = dict_split[1]
            galleryinfo.append(tmp_dic)

        self.total_page = len(galleryinfo)
        self.zero_fill = len(str(self.total_page)) + 1

        return galleryinfo

    def make_dir(self):
        try:
            os.rmdir(".\\" + self.zipfilename)
        except:
            pass
        os.mkdir(self.zipfilename)
        print("dir create")

    def zip_dir(self):
        dir_name = ".\\" + self.zipfilename
        fantasy_zip = zipfile.ZipFile(self.zipfilename + ".zip", 'w')
        for folder, subfolders, files in os.walk(dir_name):
            for file in files:
                if file.endswith('.jpg'):
                    fantasy_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), dir_name), compress_type = zipfile.ZIP_DEFLATED)
 
        fantasy_zip.close()
        print("zip complete")
        
    def dir_del(self):
        for i in range(self.total_page):
            file_name = str(i).zfill(self.zero_fill) + ".jpg"
            os.remove(".\\" + self.zipfilename + "\\" + file_name)
        os.rmdir(".\\" + self.zipfilename)
        print("del complete")

    def download_data(self, galleryinfo):
        C = common.common()

        for i in range(self.total_page):
            source = C.url_from_url_from_hash(self.galleryid, galleryinfo[i], 'webp')
            img = C.url_from_url_from_hash(self.galleryid, galleryinfo[i])

            HOST = self.https + "//" + source.split("/")[2]
            URL = self.https + source

            s = requests.Session()
            s.mount(HOST, HTTP20Adapter())
            r = s.get(URL, headers=self.header, cookies=self.cookie)

            if r.status_code == 200:
                img = r._content
                file_name = str(i).zfill(self.zero_fill) + ".jpg"
                print(file_name + " download complete (" + str(i+1) + "/" + str(self.total_page) + ")")
                with open(".\\" + self.zipfilename + "\\" + file_name, 'wb') as f:
                    f.write(img)
        
        print("download complete")
    