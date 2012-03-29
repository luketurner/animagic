from urllib.request import urlopen

import lxml.html

def _search(term):
    html = lxml.html.parse("http://www.nyaa.eu/?page=search&term={0}".format(term)).getroot()
    return html

def _result_type(html):

    if html.cssselect(".tinfodownloadbutton a"):
        return "info"
    elif html.cssselect(".tlistdownload a"):
        return "list"
    else:
        return "empty"

def _download_from_list_page(html, term):
    for title_node in html.cssselect(".tlistname a"):
        if title_node.text_content() == term:
            download_node = title_node.xpath("../..")[0].cssselect(".tlistdownload a")[0]
            torrent_url = download_node.get("href")
            torrent = urlopen(torrent_url).read()
            return torrent
    print("[ERR]: Page is a search result list, but the term we want doesn't seem to be in it.")
    return False

def _download_from_info_page(html, term):
    torrent = urlopen(html.cssselect(".tinfodownloadbutton a")[0].get("href")).read()
    return torrent

def has_torrent(term):
    html = _search(term)
    page_type = _result_type(html)
    if page_type == "info":
        return True
    elif page_type == "list":
        for title_node in html.cssselect(".tlistname a"):
            if title_node.text_content() == term:
                return True
        return False
    else:
        return False

# Returns torrent information or False
def get_torrent(term):
    html = _search(term)
    page_type = _result_type(html)
    if page_type == "info":
        return _download_from_info_page(html, term)
    elif page_type == "list":
        return _download_from_list_page(html, term)
    else:
        # does not exist (empty list page)
        return False
