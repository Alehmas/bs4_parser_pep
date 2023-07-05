from requests import RequestException

from exceptions import ParserFindTagException


def get_response(session, url):
    """Trap RequestException errors."""
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        response.raise_for_status()
        return response
    except RequestException:
        raise RequestException(
            f'There was an error loading page {url}')


def find_tag(soup, tag, attrs=None):
    """Catch tag search error"""
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Tag not found {tag} {attrs}'
        raise ParserFindTagException(error_msg)
    return searched_tag
