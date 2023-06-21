import pytest
import requests
import requests_mock
import bs4
from conftest import MAIN_DOC_URL
try:
    from src import utils
except ModuleNotFoundError:
    assert False, 'Make sure there is a `utils.py` file in the `src` directory'
except ImportError:
    assert False, 'Make sure there is a `utils.py` file in the `src` directory'


def test_find_tag(soup):
    got = utils.find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    assert isinstance(got, bs4.element.Tag), (
        'The `find_tag` function in the `utils.py` module must return the tag you are looking for'
    )
    assert (
        '<section id="what-s-new-in-python">' in got.__str__()
    ), (
        'Function `find_tag` of module `utils.py` '
        'did not return expected <section> with `id=what-s-new-in-python`'
    )


def test_find_tag_exception(soup):
    with pytest.raises(BaseException) as excinfo:
        utils.find_tag(soup, 'unexpected')
    assert excinfo.typename == 'ParserFindTagException', (
        'The `find_tag` function in the `utils.py` module in case '
        'lack of searched tag'
        'should throw a non-standard `ParserFindTagException`'
    )
    msg = 'Tag not found unexpected None'
    assert msg in str(excinfo.value), (
        f'Non-standard exception should show the message: `{msg}`'
    )


def test_get_response(mock_session):
    with requests_mock.Mocker() as mock:
        mock.get(
            MAIN_DOC_URL + 'unexisting_page/',
            text='You are breathtaken',
            status_code=200
        )
        got = utils.get_response(
            mock_session,
            MAIN_DOC_URL + 'unexisting_page/'
        )
        assert isinstance(got, requests.models.Response), (
            'Make sure the `get_response` function in the `utils.py` module'
            'makes a request to the page and returns a response. \n'
            'By the way: You are breathtaken!'
        )
