def get_filename(torrent):
    return torrent.split("4:name")[1].strip('1234567890').strip(":").split("12:piece length")[0]
