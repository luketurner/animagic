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
        fm = re.escape(a["local"]).replace('\{episode\}', '(\d+)')
        m = re.search(fm, f)
        if m:
            if a['title'] not in anime_list or int(m.group(1)) > anime_list[a['title']]:
                anime_list[a['title']] = int(m.group(1))
    return anime_list

