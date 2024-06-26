# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) 
and we adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2024-06-26

### Fixed

- Wheel contains the module again.

## [1.0.0] - 2024-06-21 [YANKED]

### Added

- Mark as compatible with Python 3.12.

### Changed

- Package is now a `pyproject.toml` project instead of using `setup.py`.
- Replace outdated `xmlrunner` package for tests with `unittest-xml-reporting`.

## [0.3.0] - 2023-06-08

### Added

- Mark as compatible with Python 3.11.

### Changed

- Client: Allow bytes contents for uploading compose files.
- Requests now time out instead of potentially hanging forever.
- Instance deletion no longer returns an Instance with updated state, but 
  a boolean, to fit with Entity return type.

### Removed

- Support for Python 2.7 dropped.

## [0.2.13] - 2019-05-02

### Changed

- Build: Do not use internal pip modules to parse requirements file for setup.

### Security

- Client: Avoid unsafe YAML loading.

## [0.2.12] - 2017-12-14

### Changed

- Build: Make `builtins` module from `future` library optional during setup.

## [0.2.11] - 2017-12-14

### Changed

- Build: Include `requirements.txt` in distributable source package.

## [0.2.10] - 2017-12-14

### Changed

- Build: Do not load package during setup, instead store version separately.

## [0.2.9] - 2017-10-27

### Fixed

- Client: Handle unauthenticated API requests more cleanly by detecting the 
  status code and raising `ValueError` with the response message.

## [0.2.8] - 2017-09-06

### Fixed

- Client: Correctly handle empty object instance application.

## [0.2.7] - 2017-07-22

### Changed

- Build: Do not add tests for distributable package.

## [0.2.6] - 2017-07-22

### Added

- Unit tests for `application`, `client`, `entity`, `instance` and `utils` 
  modules added.

### Fixed

- Updating instance with additional parameters and entities now works properly.
- Client: If an instance cannot be found in v1 API, return `None` instead of an 
  empty list.

## [0.2.5] - 2017-06-14

### Fixed

- Instance members now properly retain their context and documentation.

## [0.2.4] - 2017-06-13

### Fixed

- Client: v2 response for instances without current/desired state information 
  is now properly handled.

## [0.2.3] - 2024-06-07

### Fixed

- Client: Fix `update_instance` to transmit JSON body properly.

## [0.2.2] - 2024-06-07

### Changed

- Client: Improve error handling for non-JSON responses, using plain result 
  inexception instead.

## [0.2.1] - 2024-06-06

### Changed

- Client: Strip trailing slashes from base URL before formatting API URLs.

## [0.2.0] - 2024-06-06

### Added

- Support for Python 3+ added.
- Instance: Add string representation.
- Initial release of version with feature-complete API.

[Unreleased]: 
https://github.com/grip-on-software/bigboat-python-api/compare/v0.3.0...HEAD
[0.3.0]: 
https://github.com/grip-on-software/bigboat-python-api/compare/v0.2.13...v0.3.0
[0.2.13]: 
https://github.com/grip-on-software/bigboat-python-api/compare/v0.2.12...v0.2.13
[0.2.12]: 
https://github.com/grip-on-software/bigboat-python-api/compare/v0.2.11...v0.2.12
[0.2.11]: 
https://github.com/grip-on-software/bigboat-python-api/compare/v0.2.10...v0.2.11
[0.2.10]: 
https://github.com/grip-on-software/bigboat-python-api/compare/v0.2.9...v0.2.10
[0.2.9]: 
https://github.com/grip-on-software/bigboat-python-api/compare/v0.2.8...v0.2.9
[0.2.8]: 
https://github.com/grip-on-software/bigboat-python-api/compare/v0.2.7...v0.2.8
[0.2.7]: 
https://github.com/grip-on-software/bigboat-python-api/compare/v0.2.6...v0.2.7
[0.2.6]: 
https://github.com/grip-on-software/bigboat-python-api/compare/v0.2.5...v0.2.6
[0.2.5]: 
https://github.com/grip-on-software/bigboat-python-api/compare/v0.2.4...v0.2.5
[0.2.4]: 
https://github.com/grip-on-software/bigboat-python-api/compare/v0.2.3...v0.2.4
[0.2.3]: 
https://github.com/grip-on-software/bigboat-python-api/compare/v0.2.2...v0.2.3
[0.2.2]: 
https://github.com/grip-on-software/bigboat-python-api/compare/v0.2.1...v0.2.2
[0.2.1]: 
https://github.com/grip-on-software/bigboat-python-api/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/grip-on-software/bigboat-python-api/tag/v0.2.0
[YANKED]: https://pypi.org/help/#yanked
