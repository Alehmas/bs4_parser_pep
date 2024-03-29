import logging
import re
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, DOWNLOADS_URL, EXPECTED_STATUS, MAIN_DOC_URL,
                       PEP_NEW_URL, WHATS_NEW)
from exceptions import ParserFindTagException
from outputs import control_output
from utils import find_tag, get_response


def whats_new(session):
    """Collect links to articles about innovations in Python, go through
    them and take information about the authors and editors of articles. """
    response = get_response(session, WHATS_NEW)
    soup = BeautifulSoup(response.text, 'lxml')
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'})
    results = [('Link to Article', 'Title', 'Editor, Author')]
    for section in tqdm(sections_by_python):
        version_a_tag = section.find('a')
        href = version_a_tag['href']
        version_link = urljoin(WHATS_NEW, href)
        response = get_response(session, version_link)
        if response is None:
            continue
        soup_href = BeautifulSoup(response.text, 'lxml')
        h1 = find_tag(soup_href, 'h1')
        dl = find_tag(soup_href, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append((version_link, h1.text, dl_text))
    return results


def latest_versions(session):
    """Collect information about Python version statuses."""
    response = get_response(session, MAIN_DOC_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    sidebar = find_tag(soup, 'div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
        else:
            raise ParserFindTagException('Nothing was found')
    results = [('Link to documentation', 'Version', 'Status')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (link, version, status)
        )
    return results


def download(session):
    """Download an archive with up-to-date documentation."""
    response = get_response(session, DOWNLOADS_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    main_tag = find_tag(soup, 'div', {'role': 'main'})
    table_tag = find_tag(main_tag, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag, 'a', {'href': re.compile(r'.+pdf-a4\.zip$')})
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(DOWNLOADS_URL, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'The archive has been loaded and saved: {archive_path}')


def pep(session):
    """Collect data on all PEPs, parse and saves to csv file."""
    configure_logging()
    response = get_response(session, PEP_NEW_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    section_table = soup.find('section', {'id': 'numerical-index'})
    table_date = section_table.find('tbody')
    list_date = table_date.find_all('tr')
    count_pep = 0
    count_list = {}
    count_list['Status'] = 'Quantity'
    for i in tqdm(list_date):
        pep_href = i.find('a', {'class': 'pep'})['href']
        status_main_date = i.contents[0].text
        pep_link = urljoin(PEP_NEW_URL, pep_href)
        response = session.get(pep_link)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        main_section = soup.find('section', {'id': 'pep-content'})
        pep_table = main_section.find('dl').contents
        pep_status = ''
        for y in range(1, len(pep_table), 2):
            if pep_table[y].text == 'Status:':
                pep_status = pep_table[y+2].text
        if len(status_main_date) > 1:
            status = status_main_date[1:]
            if pep_status not in EXPECTED_STATUS[status]:
                logging.info(f'Mismatched status: {pep_link} '
                             f'Status in the card: {pep_status} '
                             f'Expected statuses: {EXPECTED_STATUS[status]}')
        if pep_status not in count_list:
            count_list[pep_status] = 1
        else:
            count_list[pep_status] += 1
        count_pep += 1
    count_list['Total'] = count_pep
    return list(count_list.items())


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    """Build and execute the entire program."""
    configure_logging()
    logging.info('Parser started!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Command line arguments: {args}')
    try:
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
        logging.info('The parser has finished.')
    except Exception as err:
        logging.exception(err)


if __name__ == '__main__':
    main()
