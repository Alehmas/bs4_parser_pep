import pytest

from pathlib import Path

BASE_DIR = Path(__name__).absolute().parent
MAIN_DIR = BASE_DIR / 'src'


@pytest.fixture
def results_dir():
    return [
        d for d in MAIN_DIR.iterdir() if d.is_dir() and d.name == 'results'
    ]


def test_results_dir_exists(results_dir):
    assert len(results_dir), (
        'Folder /results not found'
    )


def test_csv_files(results_dir):
    csv_files = [
        file for file in results_dir[0].iterdir() if file.glob('*.csv')
    ]

    assert len(csv_files), (
        'Csv file not found in results folder. '
        'Save the results of the parser '
        'in a csv file in the results folder.'
    )
    assert not len(csv_files) > 1, (
        'The results folder contains more than one file. '
        'Leave only one parsing result file in this directory.'
    )
