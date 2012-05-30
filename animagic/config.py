"""
Config list take the following form:
    title: Example
    features: [title: Example, distributor: ExampleSubs, ...]
    formatstring: [web: Example Formatstring, local: Optional Local Formatstring]
    local: formatted local formatstring
    web: formatted web formatstring
"""


from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

def parse_config(datafile):

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
