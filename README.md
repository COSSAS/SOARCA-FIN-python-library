# SOARCA Fin Library
A Python implementation for the SOARCA FIN, compatible with: SOARCA the TNO orchestrator for Open-C2, CACAO and STIX
For more information about the SOARCA, we refer the reader to the [website](https://cossas.github.io/SOARCA/) of the SOARCA project.
For more in depth documentation, see the documentation page on here.

## Quick Use

Usage of this SOARCA Fin Library is described [here](https://cossas.github.io/SOARCA/docs/soarca-extensions/fin-python-library/).

## Example 

An example is given in this project in the file `examples/pong_example.py`

## Contributing
Want to contribute to this project? Please keep in mind the following [rules](https://cossas.github.io/SOARCA/docs/contribution-guidelines/):
- This repository uses git **rebase** strategy
- For each PR, there should be at least one issue
- Make sure all tests pass (including lint errors)

### Running this repository
#### Requirements
 - Python3
 - Poetry

#### Setup
##### Env File
In order to run the project, create an `.env` file in the root of the project with the following entries:
```bash
MQTT_BROKER = "{INSERT_MQTT_BROKER_URL_HERE}"
MQTT_PORT = "{INSERT_MQTT_PORT_HERE}"
MQTT_USERNAME = "{INSERT_USERNAME_HERE}"
MQTT_PASSWD = "{INSERT_PASSWORD_HERE}"
```
If no `.env` file is specified, the following default values will be used:
```bash
MQTT_BROKER = "localhost"
MQTT_PORT = "1883"
MQTT_USERNAME = "soarca"
MQTT_PASSWD = "password"
```

##### Dependencies
To handle dependencies in this project, the package Poetry is used.
To install Poetry execute the following command:
```bash
pip3 install poetry
```

To install the dependencies from the `pyproject.toml` either enter a poetry shell, create a virtual environment or use poetry run.
To enter a poetry shell execute the following command in the root of the project:
```bash
poetry shell
```

To install the dependencies in a poetry shell or create a virtual environment, run:
```bash
poetry install
```

### Quick Run
To quick run the project, either run it through poetry run or a poetry shell.
#### Poetry Run
```bash
poetry run python examples/pong_example.py
```

#### Poetry Shell
```bash
python examples/pong_example.py
```

### Running tests
To run the tests in this repository use:
```bash
poetry run python -m unittest
``` 
To run python linter, first install pylint and then run pylint with the following arguments:
```bash
poetry add pylint &&
poetry run pylint --disable=R,C $(git ls-files '*.py')
```
To format the code base, first install ruff and then run ruff:
```bash
poetry add ruff &&
poetry run ruff format
```
