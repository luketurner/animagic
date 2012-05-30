import itertools
import os
import re

def _get_filenames(wd='.'):
    it = (files for _, _, files in os.walk(wd))
    return itertools.chain.from_iterable(it)

# Returns dict of anime titles to their max. local episode number
def anime(ac, wd="."):
    files = _get_filenames(wd)
    anime_list = {}

    for f, a in itertools.product(files, ac):
        search_regex = re.escape(a["local"])
        search_regex = re.sub('\\\{episode.*\\\}', '(\d+)', search_regex)
        match = re.search(search_regex, f)
        if match:
            if a['title'] not in anime_list:
                anime_list[a['title']] = [int(match.group(1))]
            elif int(match.group(1)) not in anime_list[a['title']]:
                anime_list[a['title']].append(int(match.group(1)))
    return anime_list

