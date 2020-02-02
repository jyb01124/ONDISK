import hashlib, time
from hyper.contrib import HTTP20Adapter, HTTPAdapter
import chilkat, requests
from bs4 import BeautifulSoup

class node_:
    keys = []
    datas = []
    subnode_addresses = []

class search:
    query = ""
    domain = "ltn.hitomi.la"
    galleries_index_dir = "galleriesindex"
    separator = '-'
    extension = '.html'
    galleriesdir = 'galleries'
    index_dir = 'tagindex'
    galleries_index_dir = 'galleriesindex'
    galleryblock = 'galleryblock'
    max_node_size = 464
    B = 16
    search_serial = 0
    search_result_index = -1
    compressed_nozomi_prefix = 'n'
    version = 0
    galleries_index_version = 0

    def set_query(self, query):
        self.query = query

    def query2version(self, name):
        url = "https://" + self.domain + "/" + name + "/version?_=" + str(int(time.time()))
        resp = requests.get(url)
        version = resp.content.decode("utf-8")
        return version

    def decode_node(self, data):
        N = node_()
        pos = 0
        number_of_keys = int.from_bytes(data[pos:pos+4], "big")

        pos += 4
        keys = []
        
        i = 0
        while (i < number_of_keys):
            key_size = int.from_bytes(data[pos:pos+4], "big")
            if (0 >= key_size) or (key_size > 32):
                print("fatal: !key_size || key_size > 32")
                return None
            pos += 4
            keys.append([int.from_bytes(data[pos:pos+1], "big"), int.from_bytes(data[pos+1:pos+2], "big"), int.from_bytes(data[pos+2:pos+3], "big"), int.from_bytes(data[pos+3:pos+4], "big")])
            pos += key_size
            i += 1

        number_of_datas = int.from_bytes(data[pos:pos+4], "big")
        pos += 4

        datas = []
        i = 0
        while (i < number_of_datas):
            offset = int.from_bytes(data[pos:pos+8], "big")
            pos += 8

            length = int.from_bytes(data[pos:pos+4], "big")
            pos += 4

            datas.append([offset, length])
            i += 1

        number_of_subnode_addresses = self.B + 1
        subnode_addresses = []

        i = 0
        while (i < number_of_subnode_addresses):
            subnode_address = int.from_bytes(data[pos:pos+8], "big")
            pos += 8

            subnode_addresses.append(subnode_address)
            i += 1

        N.keys = keys
        N.datas = datas
        N.subnode_addresses = subnode_addresses

        return N

    def get_url_at_range(self, url, Range):
        headers = {
            'accept': '*/*',
            'accept-encoding': 'identity',
            'accept-language': 'ko,ko-KR;q=0.9',
            'origin': 'https://hitomi.la',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'Range': 'bytes='+str(Range[0])+'-'+str(Range[1]),
            'Referer': 'https://hitomi.la/search.html?korean',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        host = 'https://ltn.hitomi.la/'
        s = requests.Session()
        s.mount(host, HTTP20Adapter())
        res = s.get(url, headers=headers)
        rep_code = res.status_code

        if rep_code == 200 or rep_code == 206:
            return res._content
        return None

    def get_node_at_address(self, field, address, serial=None):
        self.version = self.query2version(self.index_dir)
        url = 'https://' + self.domain + '/' + self.index_dir + '/' + field + '.' + self.version + '.index'
        if field == 'galleries':
            self.galleries_index_version = self.query2version(self.galleries_index_dir)
            url = 'https://' + self.domain + '/' + self.galleries_index_dir + '/galleries.' + self.galleries_index_version + '.index'

        rtn = self.get_url_at_range(url, [address, address + self.max_node_size-1])
        return self.decode_node(rtn)

    def compare_arraybuffers(self, dv1, dv2):
        top = min([len(dv1), len(dv2)])
        i = 0
        while (i < top):
            if dv1[i] < dv2[i]:
                return -1
            elif dv1[i] > dv2[i]:
                return 1
            i += 1
        return 0

    def locate_key(self, key, node):
        int2bool = {-1:False, 0:True, 1:False}
        cmp_result = -1
        i = 0
        while (i < len(node.keys)):
            cmp_result = self.compare_arraybuffers(key, node.keys[i]) 
            if cmp_result <= 0:
                break
            i += 1
        return [int2bool[cmp_result], i]

    def is_leaf(self, node):
        i = 0
        while (i < len(node.subnode_addresses)):
            if node.subnode_addresses[i]:
                return False
            i += 1
        return True

    def b_search(self, field, key, node, serial=None):
        if node == None:
            return False
        if len(node.keys) == 0:
            return False
        there, where = self.locate_key(key, node)
        if there:
            return node.datas[where]
        elif self.is_leaf(node):
            return False
        NN = self.get_node_at_address(field, node.subnode_addresses[where], serial)
        return self.b_search(field, key, NN, serial)

    def get_galleryids_from_data(self, data):
        if data == None:
            return []
        
        url = 'https://' + self.domain + '/' + self.galleries_index_dir + '/galleries.' + self.galleries_index_version + '.data'
        
        offset = data[0]
        length = data[1]

        if (length > 100000000) or (length <= 0):
            print("length "+length+" is too long") 
            return []

        inbuf = self.get_url_at_range(url, [offset, offset+length-1])
        if inbuf == None:
            return []
        
        galleryids = []
        pos = 0

        number_of_galleryids = int.from_bytes(inbuf[pos:pos+4], "big")
        pos += 4

        expected_length = number_of_galleryids * 4 + 4
        if (number_of_galleryids > 10000000) or (number_of_galleryids <= 0):
            print("number_of_galleryids "+number_of_galleryids+" is too long")
            return []
        elif (len(inbuf) != expected_length):
            print("inbuf.byteLength "+len(inbuf)+" !== expected_length "+expected_length)
            return []

        i = 0
        while (i < number_of_galleryids):
            galleryids.append(int.from_bytes(inbuf[pos:pos+4], "big"))
            pos += 4
            i += 1
        
        return galleryids

    def get_galleryids_for_query(self):
        self.query2sha = str(hashlib.sha256(self.query.encode()).hexdigest())[:8]
        key = [ int(self.query2sha[:2], 16), int(self.query2sha[2:4], 16), int(self.query2sha[4:6], 16), int(self.query2sha[6:8], 16) ]
        field = "galleries"
        node = self.get_node_at_address(field, 0)
        if node == None:
            return []
        data = self.b_search(field, key, node)
        if data == None:
            return []
        rtn = self.get_galleryids_from_data(data)
        return rtn

    def extract2TAG(self, code_num):
        url = "https://" + self.domain + "/" + self.galleryblock + "/" + str(code_num) + self.extension
        r = requests.get(url)
        words = str(r.text)
        h1_a = BeautifulSoup(words, 'html.parser').find_all("h1", class_="lillie")[0].string
        td_relatedtags = BeautifulSoup(words, 'html.parser').find_all("td", class_="relatedtags")
        for i in td_relatedtags:
            As = BeautifulSoup(str(i), 'html.parser').find_all("a", href=True)
            for j in As:
                if "loli" in str(BeautifulSoup(str(j), 'html.parser').string):
                    return None
        return h1_a



