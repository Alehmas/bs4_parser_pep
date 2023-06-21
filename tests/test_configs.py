import pytest
import argparse
try:
    from src import configs
except ModuleNotFoundError:
    assert False, 'Make sure there is a `configs.py` file in the `src` directory'
except ImportError:
    assert False, 'Make sure there is a `configs.py` file in the `src` directory'


def test_configs_file():
    assert hasattr(configs, 'configure_argument_parser'), (
        'Add the function `configure_argument_parser` to the `configs.py` module.'
    )
    assert hasattr(configs, 'configure_logging'), (
        'Add the `configure_logging` function to the `configs.py` module.'
    )


@pytest.mark.parametrize('action, option_string, dest, choises, help_str', [
    (
        argparse._StoreAction, [], 'mode',
        ['whats-new', 'latest-versions', 'download', 'pep'],
        'Parser Modes'
    ),
    (
        argparse._StoreTrueAction, ['-c', '--clear-cache'], 'clear_cache',
        None, 'Clear cache'
    ),
    (
        argparse._StoreAction, ['-o', '--output'], 'output',
        ('pretty', 'file'),
        'Additional output methods'
    ),
])
def test_configure_argument_parser(
        action,
        option_string,
        dest,
        choises,
        help_str
):
    got = configs.configure_argument_parser(choises)
    got_actions = [
        g for g in got._actions
        if isinstance(g, action) and g.dest == dest
    ]
    if not len(got_actions):
        assert False, (
            f'Check parser arguments. cli argument {dest} not '
            'corresponds to the task'
        )
    got_action = got_actions[0]
    assert isinstance(got_action, action)
    assert got_action.option_strings == option_string, (
        f'Specify a name or flag={option_string} for the argument {got_action.help}'
    )
    assert got_action.dest == dest, (
        f'Specify an attribute name for {got_action.help}'
    )
    assert got_action.choices == choises, (
        f'Specify choice for cli argument {got_action.dest}'
    )
    assert got_action.help == help_str, (
        f'Specify the cli help line of the argument {got_action.dest}'
    )
