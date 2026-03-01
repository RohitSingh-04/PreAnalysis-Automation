import urllib.parse
from functools import lru_cache
from app.settings import STRING_SEARCH_TEXT

@lru_cache(maxsize=32)
def google_search_url(query):
    return "https://google.com/search?q="+urllib.parse.quote_plus(query)


def google_name_address_url(name, address):
    return google_search_url(name + " + " + address)


@lru_cache(maxsize=32)
def google_string_search_url(name):
    return "https://google.com/search?q="+urllib.parse.quote_plus(f'\"{name}\"{STRING_SEARCH_TEXT}')

