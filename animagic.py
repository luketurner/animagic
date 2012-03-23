# This file is probably going to have the following things:

# Config file parser to interpret list of anime and its identifying characteristics
# Nyaa.eu crawler (threaded?)
# Torrent downloading thing. (threaded)
# Some kind of thing to diff the anime episodes you already have, with out list from Nyaa.
import re
import lxml.html
from urllib2 import urlopen

from yaml import load
try:
    from yaml import CLoader as Loader
except:
    from yaml import Loader

# Note: defines three new keys in the hashes: local, web, and title.
def load_anime_data(datafile):
    open(datafile)
    data = load(datafile.read(), Loader=Loader)
    datafile.close()
    for anime in data:
        anime['title'] = anime['features']['title']

        if anime['formatstring'].has_key(['local']):
            anime['local'] = anime['formatstring']['local'].format(**anime['features'])
        else:
            anime['local'] = anime['formatstring']['web'].format(**anime['features'])

        anime['web'] = anime['formatstring']['web'].format(**anime['features'])

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

# FIXME probably not working at the moment
def local_anime_index(wd='.'):
    fnames = []
    for i in os.listdir(wd):
        if not (i == "." or i == ".."):
            if os.isdir(i):
                fnames = local_anime_index(i)

def main():
    anime = load_anime_data("config.yaml")
