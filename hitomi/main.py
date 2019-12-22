import hitomi

gal_num = 1538234
zipfilename = "asdf"
H = hitomi.hitomi()
H.input_data(gal_num, zipfilename)
galleryinfo = H.galleryinfo_download()
H.make_dir()
H.download_data(galleryinfo)
H.zip_dir()
H.dir_del()