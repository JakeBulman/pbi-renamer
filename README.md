# python-utilities

## Getting Started

### Prerequisites
- Have an up-to-date version of Python installed (3.10.2 from the SC)
- Ideally, have Visual Studio Code installed

###  Install
- Install Python dependencies
```sh
pip install -r requirements.txt
```

### Usage
- Place a .pbip fileset into ./powerbi-renamer/target-pbi/ (see ./powerbi-renamer/test-pbi/ for an example)
- The code is run from program.py
```sh
python powerbi-renamer/src/program.py
```

### Testing
- This repository can be tested using pytest, which is installed as part of the dependencies
```py
pytest
```
or
```sh
python -m pytest
```

- You can check the test coverage of this project through pytest-cov
```sh
pytest --cov=powerbi-renamer
```