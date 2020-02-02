import hitomi, search

S = search.search()
H = hitomi.hitomi()
S.set_query("korean")
codes = S.get_galleryids_for_query()

for i in codes:
    title = S.extract2TAG(i)
    if title  == None:
        continue
    print(title)
    H.input_data(int(i), title)
    galleryinfo = H.galleryinfo_download()
    H.make_dir()
    H.download_data(galleryinfo)
    H.zip_dir()
    H.dir_del()
