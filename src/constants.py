from pathlib import Path
from urllib.parse import urljoin

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / 'logs'
RESULTS_DIR = BASE_DIR / 'results'

MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_NEW_URL = 'https://peps.python.org/'
WHATS_NEW = urljoin(MAIN_DOC_URL, 'whatsnew/')
DOWNLOADS_URL = urljoin(MAIN_DOC_URL, 'download.html')

LOG_FILE = LOG_DIR / 'parser.log'

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

EXPECTED_STATUS = {
    'A': ['Active', 'Accepted'],
    'D': ['Deferred'],
    'F': ['Final'],
    'P': ['Provisional'],
    'R': ['Rejected'],
    'S': ['Superseded'],
    'W': ['Withdrawn'],
    '': ['Draft', 'Active'],
}
PRETTY = 'pretty'
FILE = 'file'
