import pytest
from pathlib import Path
try:
    from src import main
except ModuleNotFoundError:
    assert False, 'Make sure there is a `main.py` file in the `src` directory'
except ImportError:
    assert False, 'Make sure there is a `main.py` file in the `src` directory'


def test_main_file():
    assert hasattr(main, 'whats_new'), (
        'Add the `whats_new` function to the `main.py` module.'
    )
    assert hasattr(main, 'latest_versions'), (
        'Add the `latest_versions` function to the `main.py` module.'
    )
    assert hasattr(main, 'download'), (
        'Add a `download` function to the `main.py` module.'
    )
    assert hasattr(main, 'pep'), (
        'Add the `pep` function to the `main.py` module.'
    )
    assert hasattr(main, 'MODE_TO_FUNCTION'), (
        'Add a `MODE_TO_FUNCTION` dictionary listing modes '
        'parser work.'
    )
    assert hasattr(main, 'main'), (
        'Add the `main` function to the `main.py` module.'
    )


def test_whats_new(mock_session):
    got = main.whats_new(mock_session)
    header = ('Link to Article', 'Title', 'Editor, Author')
    assert isinstance(got, list), (
        'The `whats_new` function must return an object of type `list`'
    )
    assert len(got) > 0, (
        'Make sure the function `whats_new` of module `main.py` '
        'returns a non-empty list'
    )
    assert isinstance(got[0], tuple), (
        'The `whats_new` function should return a list of `result`, '
        'whose elements must be objects of type `tuple`'
    )
    assert header in got, (
        'In the `whats_new` function, the first element in the `result` list is '
        'must be a tuple '
        '(`Link to article`, `Title`, `Editor, Author`)'
    )



def test_latest_versions(mock_session):
    got = main.latest_versions(mock_session)
    assert isinstance(got, list), (
        'The `latest_versions` function must return an object of type `list`'
    )
    assert isinstance(got[0], tuple), (
        'The `latest_versions` function should return a list of `result`, '
        'whose elements must be objects of type `tuple`'
    )
    header = ('Link to documentation', 'Version', 'Status')
    answer = [
        ('Link to documentation', 'Version', 'Status'),
        ('https://docs.python.org/3.13/', '3.13', 'in development'),
        ('https://docs.python.org/3.12/', '3.12', 'pre-release'),
        ('https://docs.python.org/3.11/', '3.11', 'stable'),
        ('https://docs.python.org/3.10/', '3.10', 'security-fixes'),
        ('https://docs.python.org/3.9/', '3.9', 'security-fixes'),
        ('https://docs.python.org/3.8/', '3.8', 'security-fixes'),
        ('https://docs.python.org/3.7/', '3.7', 'security-fixes'),
        ('https://docs.python.org/3.6/', '3.6', 'EOL'),
        ('https://docs.python.org/3.5/', '3.5', 'EOL'),
        ('https://docs.python.org/2.7/', '2.7', 'EOL'),
        ('https://www.python.org/doc/versions/', 'All versions', '')
    ]
    assert header in got, (
        'In the `latest_versions` function in the results list '
        'the first element must be a tuple '
        '`Documentation Link, Version, Status`'
    )
    assert got == answer, (
        'The `latest_versions` function should return '
        f'an object of the form ```{answer}```'
    )


def test_download(monkeypatch, tmp_path, mock_session):
    mock_base_dir = Path(tmp_path)
    monkeypatch.setattr(main, 'BASE_DIR', mock_base_dir)
    got = main.download(mock_session)
    dirs = [
        directory for directory in mock_base_dir.iterdir()
        if directory.is_dir() and directory.name == 'downloads'
    ]

    assert len(dirs) != 0, (
        'Make sure to store Python documentation archives in '
        'directory `src` creates a directory `downloads` '
    )
    output_files = [
        f for f in mock_base_dir.glob('**/*') if str(f).endswith('.zip')
    ]
    assert len(output_files) != 0, (
        'Make sure the Python documentation archive is loaded'
        'to the directory `src/downloads` '
    )
    assert got is None, (
        'The `download` function in the `main.py` module must not return a value.',
        'The function should only load and save the archive.'
    )


def test_mode_to_function():
    got = main.MODE_TO_FUNCTION
    assert isinstance(got, dict), (
        'In the `main.py` module, the `MODE_TO_FUNCTION` object must be a dictionary'
    )
    for name_func, func in got.items():
        assert isinstance(name_func, str), (
            'Make sure that in module `main.py` `MODE_TO_FUNCTION` '
            f'{name_func} is a string.'
        )
        assert (
            name_func in ['whats-new', 'latest-versions', 'download', 'pep']
        ), (
            'In module `main.py` in object `MODE_TO_FUNCTION` '
            f'no key `{name_func}`'
        )
        assert callable(func), (
            'Make sure that in module `main.py` in object `MODE_TO_FUNCTION` '
            f'`{func}` is a function.'
        )
        assert (
            func.__name__ in [
                'whats_new', 'latest_versions', 'download', 'pep'
            ]
        ), (
            'In module `main.py` in object `MODE_TO_FUNCTION` '
            f'no value {func}'
        )
