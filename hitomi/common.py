import re
class common:
    adapose = False
    number_of_frontends = 3
    loading_timer = None
    domain = "(/^dev\./.test(document.location.hostname.toString()) ? 'dev' : 'ltn')+'.hitomi.la'"
    galleryblockextension = '.html'
    galleryblockdir = 'galleryblock'
    nozomiextension = '.nozomi'

    def js_posix_exec(self, r, url):
        r_ = r.search(url)
        posix_dict = {}
        if r_ == None:
            return False
        posix_dict["index"] = r_.start()
        posix_dict["input"] = r_.string
        posix_dict[0] = r_.group()
        cnt = 1
        for i in r_.groups():
            posix_dict[cnt] = i
            cnt += 1
        
        return posix_dict

    def isNaN(self, s):
        try:
            float(s)
            return False
        except ValueError:
            return True

    def subdomain_from_galleryid(self, g):
        if self.adapose:
            return '0'
        o = g % self.number_of_frontends
        return chr(97 + o)

    def subdomain_from_url(self, url, base):
        retval = 'a'
        if base:
            retval = base
        
        r = re.compile("/galleries/\d*(\d)/")
        m = self.js_posix_exec(r, url)
        b = 10
        if not m:
            b = 16
            r2 = re.compile("/[0-9a-f]/([0-9a-f]{2})/")
            m = self.js_posix_exec(r2, url)
            if not m:
                return retval
        
        g = int(m[1], b)

        if not self.isNaN(g):
            retval = str(self.subdomain_from_galleryid(g)) + retval

        return retval

    def url_from_url(self, url, base=None):
        r = re.compile("//..?\.hitomi\.la/")
        pisix_result = r.findall(url)
        for i in pisix_result:
            url = url.replace(i,'//' + self.subdomain_from_url(url, base) + '.hitomi.la/')
        return url

    def full_path_from_hash(self, hash):
        if len(hash) < 3:
            return hash
        r = re.compile("^.*(..)(.)$")
        m = self.js_posix_exec(r, hash)
        return hash.replace(m[0], hash[-1:] + "/" + hash[-3:-1] + "/" + hash)

    def OR_string(self, str_1, str_2):
        if bool(str_1):
            return str_1
        elif bool(str_2):
            return str_2
        else:
            return None

    def url_from_hash(self, galleryid, image, webp):
        url = ""
        ext = self.OR_string(webp, image["name"].split(".").pop())
        webp = self.OR_string(webp, 'images')

        if bool(image["hash"]):
            url = '//a.hitomi.la/'+webp+'/'+ self.full_path_from_hash(image["hash"]) +'.'+ext
        else:
            url = '//a.hitomi.la/galleries/'+galleryid+'/'+image["name"]
        
        return url

    def url_from_url_from_hash(self, galleryid, image, webp=None):
        return self.url_from_url(self.url_from_hash(galleryid, image, webp))