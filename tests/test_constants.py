import inspect
from pathlib import Path
try:
    from src import constants
except ModuleNotFoundError:
    assert False, 'Make sure there is a `constants.py` file in the `src` directory'
except ImportError:
    assert False, 'Make sure there is a `constants.py` file in the `src` directory'


def test_costants_file():
    assert hasattr(constants, 'MAIN_DOC_URL'), (
        'There is no `MAIN_DOC_URL` variable in module `constants.py`'
    )
    assert isinstance(constants.MAIN_DOC_URL, str), (
        'In module `constants.py` variable type `MAIN_DOC_URL` '
        'must be `str`'
    )
    variables = [
        code for var, code in inspect.getmembers(constants)
        if not var.startswith('__')
    ]
    assert 'https://peps.python.org/' in variables, (
        'No variable for PEP page in module `constants.py`'
    )
    assert hasattr(constants, 'BASE_DIR'), (
        'There is no `BASE_DIR` variable in module `constants.py`'
    )
    assert isinstance(constants.BASE_DIR, Path), (
        'In module `constants.py` the type of variable `BASE_DIR` must be `Path`'
    )
    assert hasattr(constants, 'EXPECTED_STATUS'), (
        'There is no `EXPECTED_STATUS` variable in module `constants.py`'
    )
    assert isinstance(constants.EXPECTED_STATUS, dict), (
        'In module `constants.py` variable type `EXPECTED_STATUS` '
        'must be a `dict`'
    )
