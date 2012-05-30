import logging
from os.path import exists, join

from animagic import local, nyaa, config

logger = logging.getLogger(__name__)

# where anime is a dict from anime config
def _get_anime_episode(anime, episode, dirn="torrents"):

    fname = join(dirn, anime["local"].format(episode = episode) + '.torrent')
    if exists(fname):
        logger.info("%s exists. Not downloading.", fname)
        return True

    search_string = anime["web"].format(episode = episode)
    torrent = nyaa.get_torrent(search_string)
    if torrent:
        logger.info("Saving %s as %s", search_string, fname)
        local_file = open(fname, 'wb')
        local_file.write(torrent)
        local_file.close()
        return True
    else:
        logger.info("Could not find %s. Switching to next show.", search_string)
        return False

def _download_new_anime(anime_config_list, local_anime_list, torrent_dir):
    for anime in anime_config_list:
        
        episode = 1

        if episode in local_anime_list[anime['title']]:
            download_success = True
        else:
            download_success = _get_anime_episode(anime, episode, torrent_dir)

        while download_success:
            # Download the next one
            episode += 1
            if episode in local_anime_list[anime['title']]:
                download_success = True
            else:
                download_success = _get_anime_episode(anime, episode, torrent_dir)

def sync_all_anime(anime_config, anime_dir, torrent_dir):

    anime_config_list = config.parse_config(anime_config)
    local_anime_list = local.anime(anime_config_list, anime_dir)
    print(local_anime_list)

    _download_new_anime(anime_config_list, local_anime_list, torrent_dir)

