# This file is probably going to have the following things:

# Config file parser to interpret list of anime and its identifying characteristics
# Nyaa.eu crawler (threaded?)
# Torrent downloading thing. (threaded)
# Some kind of thing to diff the anime episodes you already have, with out list from Nyaa.
import itertools
import os
import re
from os.path import exists

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from animagic import local, nyaa

# Note: defines three new keys in the hashes: local, web, and title.
# local and web probably still contain {episode} to be formatted in later.
def _load_anime_config(datafile):

    with open(datafile) as f:
        data = load(f.read(), Loader=Loader)

    for anime in data:
        anime['title'] = anime['features']['title']

        features = anime['features']

        if 'local' in anime['formatstring']:
            anime['local'] = anime['formatstring']['local'].format(**features)
        else:
            anime['local'] = anime['formatstring']['web'].format(**features)

        anime['web'] = anime['formatstring']['web'].format(**features)

    return data

def _torrent_get_filename(torrent):
    # FIXME this is terrible, but regex parsing doesn't seem to work very well. It seems to work... mostly.
    fname = torrent.split("4:name")[1].strip('1234567890').strip(":").split("12:piece length")[0]



# where anime is a dict from anime config
def _get_anime_episode(anime, episode, dirn="torrents"):

    fname = os.path.join(dirn, anime["local"].format(episode = episode) + '.torrent')
    if exists(fname):
        print("Torrent file {0} already exists".format(fname))
        return True

    search_string = anime["web"].format(episode = episode)
    torrent = nyaa.get_torrent(search_string)
    if torrent:
        print("Saving {0} as {1}".format(search_string, fname))
        local_file = open(fname, 'wb')
        local_file.write(torrent)
        local_file.close()
        return True
    else:
        print("Could not find {0}.".format(search_string))
        return False

def _download_new_anime(anime_config_list, local_anime_list, torrent_dir):
    for anime in anime_config_list:

        if anime['title'] in local_anime_list:
            episode = local_anime_list[anime['title']]
        else:
            episode = 1

        download_success = _get_anime_episode(anime, episode, torrent_dir)
        while download_success:
            # Download the next one
            episode += 1
            download_success = _get_anime_episode(anime, episode, torrent_dir)

def get_all_new_anime(anime_config, anime_dir, torrent_dir):
    anime_config_list = _load_anime_config(anime_config)
    local_anime_list = local.anime(anime_config_list, anime_dir)

    _download_new_anime(anime_config_list, local_anime_list, torrent_dir)

