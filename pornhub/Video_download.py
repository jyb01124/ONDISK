import requests, time, datetime

class video_download:
    header = {
        "accept": "*/*",
        "accept-encoding": "identity;q=1, *;q=0",
        "accept-language": "ko,ko-KR;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "range": "bytes=0-",
        "referer": "",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "same-origin",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
    }

    def __init__(self):
        super().__init__()

    def set_param(self, url):
        print("Video_download : " + url)
        self.header["referer"] = url
        self.R = requests.get(url, stream=True)#, headers=self.header)

    def url_confirm(self, title):
        self.file_length = int(self.R.headers["content-length"])
        self.file_name = "./video/" + title + ".mp4"
        print("Video_download : " + str(self.file_length))
        stat = self.R.status_code
        if int(stat / 100) == 2:
            return 0
        print("Video_download : " + str(stat) + " " + str(datetime.datetime.now()))
        return 1

    def file_down(self):
        size = 0
        chk_time = time.time()
        with open(self.file_name, 'wb') as f:
            for chunk in self.R.iter_content(chunk_size=1024 *36):
                if chunk:
                    size += 1024 *36
                    f.write(chunk)
                if (time.time() - chk_time) > 10:
                    print("Video_download : " + str(int((size/self.file_length)*100))+"%")
                    chk_time = time.time()
    '''
    def http2_file_down(self):
        s = requests.Session()
        s.mount(HOST, HTTP20Adapter())
        r = s.get(URL, headers=self.header, cookies=self.cookie)

        if r.status_code == 200:
            img = r._content
            file_name = str(i).zfill(self.zero_fill) + ".jpg"
            print(file_name + " download complete (" + str(i+1) + "/" + str(self.total_page) + ")")
            with open(".\\" + self.zipfilename + "\\" + file_name, 'wb') as f:
                f.write(img)
    '''