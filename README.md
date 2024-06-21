# BigBoat docker dashboard Python API

[![PyPI](https://img.shields.io/pypi/v/bigboat.svg)](https://pypi.python.org/pypi/bigboat)
[![Build 
status](https://github.com/grip-on-software/bigboat-python-api/actions/workflows/bigboat-python-api.yml/badge.svg)](https://github.com/grip-on-software/bigboat-python-api/actions/workflows/bigboat-python-api.yml)
[![Coverage 
Status](https://coveralls.io/repos/github/grip-on-software/bigboat-python-api/badge.svg?branch=master)](https://coveralls.io/github/grip-on-software/bigboat-python-api?branch=master)
[![Quality Gate 
Status](https://sonarcloud.io/api/project_badges/measure?project=grip-on-software_bigboat-python-api&metric=alert_status)](https://sonarcloud.io/project/overview?id=grip-on-software_bigboat-python-api)

Python wrapper library for the BigBoat API. This API can create, retrieve, 
update and delete application definitions, do similar operations for instances 
and poll for status.

Support for v2 and the deprecated v1 APIs (limited to certain operations) is 
included. Note that BigBoat development itself has halted.

## Requirements

The BigBoat Python API has been tested to work on Python 3.8+. The API has few 
dependencies; see `requirements.txt` for the list of installation requirements. 
The short list is also repeated here:

- [Requests](http://docs.python-requests.org/en/master/user/install/)
- [PyYAML](http://pyyaml.org/wiki/PyYAMLDocumentation)

## Installation

Install the latest version from PyPI using:

```
pip install bigboat
```

For local development, you can use `pip install .` to install the package from 
the cloned Git repository.

## Functionality

First, import the library:

```python
import bigboat
```

Next, determine the URL of your BigBoat instance. In this example we use 
`http://BIG_BOAT`. Also check whether to use the v1 or v2 version of the API. 
v1 is limited (deprecated in newer versions) and v2 requires an API key. 
Example:

```python
api = bigboat.Client_v2('http://BIG_BOAT', 'MY_API_KEY')
```

You can then use various methods on the client API, namely:
- `api.apps()`: List of Applications
- `api.get_app(name, version)`: Retrieve a specific Application
- `api.update_app(name, version)`: Register an Application
- `api.delete_app(name, version)`: Delete an Application
- `api.instances()`: List of Instances
- `api.get_instance()`: Retrieve a specific Instance
- `api.update_instance(name, app_name, version, ...)`: Start an Instance
- `api.delete_instance(name)`: Stop an Instance

In addition to the common methods, v2 has the following API methods:
- `api.get_compose(name, version, file_name)`: Retrieve a docker compose or 
  bigboat compose file for an Application
- `api.update_compose(name, version, file_name, content)`: Update a docker 
  compose or bigboat compose file for an Application
- `api.statuses()`: Retrieve a list of status dictionaries

## Development

- [GitHub 
  Actions](https://github.com/grip-on-software/bigboat-python-api/actions) is 
  used to run unit tests and report on coverage for commits and pull requests.
- [SonarCloud](https://sonarcloud.io/project/overview?id=grip-on-software_bigboat-python-api) 
  performs quality gate scans and tracks them.
- [Coveralls](https://coveralls.io/github/grip-on-software/bigboat-python-api) 
  receives coverage reports and tracks them.
- You can perform local lint checks, typing checks, tests and coverage during 
  development (after setting up a local [installation](#installation)) with 
  `make pylint`, `make mypy`, `make test` and `make coverage`, respectively, 
  after installing dependencies from `requirements-analysis.txt` by running 
  `make setup_analysis` (for the `pylint` and `mypy` recipes) and from
  `requirements-test.txt` with `make setup_test` (necessary for making all the 
  Makefile recipes mentioned here function correctly).
- We publish releases to [PyPI](https://pypi.python.org/pypi/bigboat) using 
  `make release` which performs multiple checks: version number consistency, 
  lint, typing and unit tests.
- Noteworthy changes to the module are added to the [changelog](CHANGELOG.md).

## License

The API wrapper library is licensed under the Apache 2.0 License.

## References

- [Docker Dashboard](https://github.com/ICTU/docker-dashboard)
