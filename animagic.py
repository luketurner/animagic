# This file is probably going to have the following things:

# Config file parser to interpret list of anime and its identifying characteristics
# Nyaa.eu crawler (threaded?)
# Torrent downloading thing. (threaded)
# Some kind of thing to diff the anime episodes you already have, with out list from Nyaa.
import re
import lxml.html
import os
from os.path import isdir
import argparse
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
        return torrent
    except:
        print("[ERR]: Page looks like it might be formatted incorrectly.")
        return False

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
    
    for f in files:
        for a in ac:
            fm = re.escape(a["local"]).replace('\{episode\}', '(\d+)')
            m = re.search(fm, f)
            if m:
                if a['title'] not in anime_list or int(m.group(1)) > anime_list[a['title']]:
                    anime_list[a['title']] = int(m.group(1))
    return anime_list

# where anime is a dict from anime config
def get_anime_episode(anime, episode, dirn="torrents"):
    torrent = nyaa_find_torrent(anime["web"].format(episode=episode))
    if torrent:
        fname = anime["local"].format(episode=episode)
        print("Saving {0} as {1}".format(anime["web"], fname))
        local_file = open(os.path.join(dirn, fname), 'wb')
        local_file.write(torrent)
        local_file.close()
        return True
    else:
        print("Failed to save {0}".format(anime["web"]))
        return False

def find_new_anime(anime_config="config.yaml", wd="."):
    anime_config_list = load_anime_config(anime_config)
    # find local anime and then see if the local episode number + 1 exists in nyaa.eu
    local_anime_list = local_anime(anime_config_list, wd)
    for anime in anime_config_list:

        if anime['title'] in local_anime_list:
            episode = local_anime_list[anime['title']]
        else:
            episode = 1

        download_success = get_anime_episode(anime, episode)
        while download_success:
            # Download the next one
            episode += 1
            get_anime_episode(anime, episode)

def main():
    parser = argparse.ArgumentParser(description='Anime magic!')
    parser.add_argument("-c", "--config")
    parser.add_argument("-d", "--directory")
    parser.add_argument("-t", "--torrent-directory")
    #anime_config = load_anime_config()
    #local_anime_files = local_anime(anime_config, "test")
    find_new_anime();
    #print(local_anime_files)

main()
