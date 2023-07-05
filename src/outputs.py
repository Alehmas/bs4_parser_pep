import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT, FILE, PRETTY


def control_output(results, cli_args):
    """Control the output of results in the program."""
    output = cli_args.output
    if output == PRETTY:
        pretty_output(results)
    elif output == FILE:
        file_output(results, cli_args)
    else:
        default_output(results)


def default_output(results):
    """Print data line by line."""
    for row in results:
        print(*row)


def pretty_output(results):
    """Print data in table format."""
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    """Save parsing results to a csv file."""
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='unix')
        writer.writerows(results)
    logging.info(f'Result file was saved: {file_path}')
