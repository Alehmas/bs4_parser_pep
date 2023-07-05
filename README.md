# Documentation parser from docs.python.org

## Description
The parser will help you keep up to date with the latest news in the world of Python.
The parser can:
  - Collect links to articles about innovations in Python, follow them and collect information about the authors and editors of articles.
  - Gather information about Python version statuses.
  - Download archive with up-to-date documentation.
  - Collect information about all PEPs, their number, status matching and the number in each status.

## Technologies used
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## Run the parser
1.Clone the repository:
```
git clone git@github.com:Oleg-2006/yamdb_final.git
```

2.Install virtual environment:
```
python -m venv venv
```

3.Install all dependencies:
```
pip install -r requirements.txt
```

4.Go to the src folder:
```
cd src/
```

5.View all parser modes:
```
python main.py -h
```

## Parser modes
Required arguments:
- 'whats-new' - Collects links to articles about innovations in Python, follows them and takes information about the authors and editors of articles.
- 'latest-versions' - Gathers information about Python version statuses
- 'download' - Downloads an archive with up-to-date documentation.
- 'pep' - Collects information about all PEPs, their number, status matching and the number in each status.

Additional arguments:
- missing - output results to the terminal
- -c - clear cache
- -o - additional ways to output data:
     - pretty - output results to the terminal as a table
     - file - save results to csv file

## Authors
- [Aleh Maslau](https://github.com/Alehmas)