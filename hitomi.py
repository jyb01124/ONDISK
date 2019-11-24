from bs4 import BeautifulSoup
import requests, re

galleryid = 1520194
img_list_url = "https://ltn.hitomi.la/galleries/"+ str(galleryid) +".js"

response = requests.get(img_list_url)
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

js_func = "https://ltn.hitomi.la/common.js"
response = requests.get(js_func)
txt = response.content.decode('utf-8')

adapose = txt.split("var adapose")[1].split(";")[0].replace(" ","").replace("=","").replace("'","")
number_of_frontends = int(txt.split("var number_of_frontends")[1].split(";")[0].replace(" ","").replace("=","").replace("'",""))

def url_from_url_from_hash(galleryid, image, oldmethod, base):
    url = ''
    if (oldmethod != None) or (not image['hash']):
        url = '//a.hitomi.la/galleries/' + galleryid + '/' + image['name']
    else:
        hash_value = ""
        if len(image['hash']) < 3:
            hash_value = image['hash']
        else:
            hash_value = image['hash'][-1:] + "/" + image['hash'][-3:-1] + "/" + image['hash']

        ext = image['name'].split(".")
        ext = ext[len(ext)-1]
        url = '//a.hitomi.la/images/' + hash_value + '.'+ ext
    
    retval = 'a'
    rr = re.compile("\/\/..?\.hitomi\.la\/")
    OK = rr.search(url)

    if base != None: 
        retval = base
    
    r = re.compile("\/galleries\/\d*(\d)\/")
    r_result = r.search(url)

    try:
        m = [r_result.group(), r_result.groups()[0], r_result.start(), r_result.string]
    except AttributeError:
        r = re.compile("\/images\/[0-9a-f]\/([0-9a-f]{2})\/")
        r_result = r.search(url)
        try:
            m = [r_result.group(), r_result.groups()[0], r_result.start(), r_result.string]
        except:
            return url.replace(OK.group(), 'https://'+retval+'.hitomi.la/')

    try:
        g = int(m[1], 16)
    except:
        return url.replace(OK.group(), 'https://'+retval+'.hitomi.la/')
    
    c = ''
    if adapose == 'false':
        c = chr(97 + (g % number_of_frontends))
    elif adapose == 'true':
        c = '0'
    
    retval = c + retval
    return url.replace(OK.group(), 'https://'+retval+'.hitomi.la/')

page_num = 0

URL = url_from_url_from_hash(str(galleryid), galleryinfo[page_num], 'oldmethod', None)
rtl_1 = URL.replace('/galleries/', '/webp/') + '.webp'
rtl_2 = url_from_url_from_hash(str(galleryid), galleryinfo[page_num], None, None)

print(rtl_1)
print(rtl_2)





