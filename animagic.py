# This file is probably going to have the following things:

# Config file parser to interpret list of anime and its identifying characteristics
# Nyaa.eu crawler (threaded?)
# Torrent downloading thing. (threaded)
# Some kind of thing to diff the anime episodes you already have, with out list from Nyaa.
import itertools
import os
import re
from os.path import isdir, exists
from urllib.request import urlopen

import lxml.html
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

# Note: defines three new keys in the hashes: local, web, and title.
# local and web probably still contain {episode} to be formatted in later.
def load_anime_config(datafile="config.yaml"):
    with open(datafile) as f:
        data = load(f.read(), Loader=Loader)
    for anime in data:
        anime['title'] = anime['features']['title']

        #FIXME episode workaround
        features = dict(anime['features'])
        features['episode']='{episode:=02}'

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
    if html.cssselect(".tinfodownloadbutton a"):
        # Is a "single-file" page
        torrent = urlopen(html.cssselect(".tinfodownloadbutton a")[0].get("href")).read()
        return torrent
    elif html.cssselect(".tlistdownload a"):
        # is a "list" page.
        for title_node in html.cssselect(".tlistname a"):
            if title_node.text_content() == term:
                download_node = title_node.xpath("../..")[0].cssselect(".tlistdownload a")[0]
                torrent_url = download_node.get("href")
                torrent = urlopen(torrent_url).read()
                return torrent
        print("[ERR]: Page is a search result list, but the term we want doesn't seem to be in it.")
        return False
    else:
        # does not exist (empty list page)
        print("[ERR]: Page looks like it might be formatted incorrectly.")
        return False

def local_files(wd='.'):
    it = (files for _, _, files in os.walk(wd))
    return itertools.chain.from_iterable(it)

# Returns dict of anime titles to their max. local episode number
def local_anime(ac, wd="."):
    files = local_files(wd)
    anime_list = {}

    for f, a in itertools.product(files, ac):
        fm = re.escape(a["local"]).replace('\{episode\}', '(\d+)')
        m = re.search(fm, f)
        if m:
            if a['title'] not in anime_list or int(m.group(1)) > anime_list[a['title']]:
                anime_list[a['title']] = int(m.group(1))
    return anime_list

# where anime is a dict from anime config
def get_anime_episode(anime, episode, dirn="torrents"):

    fname = anime["local"].format(episode = episode) + '.torrent'
    if exists(fname):
        print("Torrent file {0} already exists".format(fname))
        return True

    search_string = anime["web"].format(episode = episode)
    torrent = nyaa_find_torrent(search_string)
    if torrent:
        print("Saving {0} as {1}".format(search_string, fname))
        local_file = open(os.path.join(dirn, fname), 'wb')
        local_file.write(torrent)
        local_file.close()
        return True
    else:
        print("Could not find {0}.".format(search_string))
        return False

def find_new_anime(anime_config, wd, torrent_dir):
    for anime in anime_config_list:

        if anime['title'] in local_anime_list:
            episode = local_anime_list[anime['title']]
        else:
            episode = 1

        download_success = get_anime_episode(anime, episode, torrent_dir)
        while download_success:
            # Download the next one
            episode += 1
            download_success = get_anime_episode(anime, episode, torrent_dir)

def get_all_new_anime(anime_config, anime_dir, torrent_dir):
    anime_config_list = load_anime_config(anime_config)
    local_anime_list = local_anime(anime_config_list, anime_dir)

    download_new_anime(anime_config, anime_dir, torrent_dir)

