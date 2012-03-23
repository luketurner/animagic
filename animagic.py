# This file is probably going to have the following things:

# Config file parser to interpret list of anime and its identifying characteristics
# Nyaa.eu crawler (threaded?)
# Torrent downloading thing. (threaded)
# Some kind of thing to diff the anime episodes you already have, with out list from Nyaa.
import re
import lxml.html
import os
from os.path import isdir
from urllib.request import urlopen

from yaml import load
try:
    from yaml import CLoader as Loader
except:
    from yaml import Loader

# Note: defines three new keys in the hashes: local, web, and title.
# local and web probably still contain {episode} to be formatted in later.
def load_anime_config(datafile="config.yaml"):
    f = open(datafile)
    data = load(f.read(), Loader=Loader)
    f.close()
    for anime in data:
        anime['title'] = anime['features']['title']

        #FIXME episode workaround
        features = dict(anime['features'])
        features['episode']='{episode}'

        if 'local' in anime['formatstring']:
            anime['local'] = anime['formatstring']['local'].format(**features)
        else:
            anime['local'] = anime['formatstring']['web'].format(**features)

        anime['web'] = anime['formatstring']['web'].format(**features)

    return data

def torrent_get_filename(torrent):
    # FIXME this is terrible, but regex parsing doesn't seem to work very well. It seems to work... mostly.
    fname = torrent.split("4:name")[1].strip('1234567890').strip(":").split("12:piece length")[0]

def nyaa_find_torrent(term):
    # Note that this brings you directly to the anime page if the search string returns exactly one result,
    #  which is our desired case anyway.
    html = lxml.html.parse("http://www.nyaa.eu/?page=search&term={0}".format(term)).getroot()
    try:
        torrent = urlopen(html.cssselect(".tinfodownloadbutton a")[0].get("href")).read()
    except:
        # page is formatted incorrectly. Could be there were more than one result from search term.
        print("[ERR]: Page looks like it might be formatted incorrectly.")
        return False
    return torrent

# TODO is there a batter way to do this?
def local_files(wd='.'):
    fnames = []
    for f in os.listdir(wd):
        if not (f == "." or f == ".."):
            if isdir(f):
                fnames += local_files(f)
            else:
                fnames.append(f)
    return fnames

# Returns dict of anime titles to their max. local episode number
def local_anime(ac, wd="."):
    files = local_files(wd)
    anime_list = {}
    
    #TODO see if there's a more efficient way to do this
    #  nested for-loop
    for f in files:
        for a in ac:
            m = re.match(f, re.sub(re.escape(a["local"]), "\{episode\}", "(\d?)"))
            if m and int(m.group(1)) > anime_list[a[title]]:
                anime_list[a[title]] = int(m.group(1))


def find_new_anime(anime_config="config.yaml"):
    anime_config_list = load_anime_data(anime_config)
    # find local anime and then see if the local episode number + 1 exists in nyaa.eu
    local_anime_list = local_anime(anime_config_list)

def main():
    anime_config = load_anime_config()
    local_anime_files = local_anime(anime_config, "/storage/Anime")
    print(local_anime_files)

main()
