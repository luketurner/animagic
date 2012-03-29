# This file is probably going to have the following things:

# Config file parser to interpret list of anime and its identifying characteristics
# Nyaa.eu crawler (threaded?)
# Torrent downloading thing. (threaded)
# Some kind of thing to diff the anime episodes you already have, with out list from Nyaa.
from os.path import exists, join

from animagic import local, nyaa, config

# where anime is a dict from anime config
def _get_anime_episode(anime, episode, dirn="torrents"):

    fname = join(dirn, anime["local"].format(episode = episode) + '.torrent')
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

def sync_all_anime(anime_config, anime_dir, torrent_dir):

    anime_config_list = config.parse_config(anime_config)
    local_anime_list = local.anime(anime_config_list, anime_dir)

    _download_new_anime(anime_config_list, local_anime_list, torrent_dir)

