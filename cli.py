import argparse

import animagic

def main():
    parser = argparse.ArgumentParser(description='Command-line frontend for animagic.')
    parser.add_argument("-c", "--config", default="config.yaml")
    parser.add_argument("-d", "--directory")
    parser.add_argument("-t", "--torrent-directory")
    parser.add_argument("task", help="The task for the script. Usually people want this to be 'sync'")
    args = parser.parse_args()

    config_file = args.config

    if args.directory:
        anime_directory = args.directory
    else:
        print("Please specify the root directory of your anime collection with -d")
        return 1

    if args.torrent_directory:
        torrent_directory = args.torrent_directory
    else:
        print("Please specify the torrent download directory with -t")
        return 1
    
    animagic.get_all_new_anime(config_file, anime_directory, torrent_directory)

if __name__ == "__main__":
    main()
