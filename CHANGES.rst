CHANGELOG
=========

.. towncrier release notes start

pytest-mongo 4.0.0 (2026-02-04)
===============================

Breaking changes
----------------

- Drop support for Python 3.9 (`#713 <https://github.com/dbfixtures/pytest-mongo/issues/713>`__)
- logsdir is no longer configurable; all temporary files are managed by tmp_path_factory. (`#742 <https://github.com/dbfixtures/pytest-mongo/issues/742>`__)
- Bumped minimum supported pytest version to 8.4 (`#745 <https://github.com/dbfixtures/pytest-mongo/issues/745>`__)


Bugfixes
--------

- Remove Mongo's DBpath only after checking for its existence at the end of the proc fixture. (`#725 <https://github.com/dbfixtures/pytest-mongo/issues/725>`__)
- Correctly register `--mongo-tz-aware` command-line option with bool type. (`#745 <https://github.com/dbfixtures/pytest-mongo/issues/745>`__)


Features
--------

- Add support for Python 3.14 (`#713 <https://github.com/dbfixtures/pytest-mongo/issues/713>`__)
- Replace TypedDict-based config with a dataclass-based config. (`#722 <https://github.com/dbfixtures/pytest-mongo/issues/722>`__)
- Improved xdist compatibility by introducing port-locking mechanism.

  If one worker will claim port, it will lock it, and other xdist workers will
  either check another port or raise error with clear message. (`#723 <https://github.com/dbfixtures/pytest-mongo/issues/723>`__)
- Temporary files for the process are now handled by tmp_path_factory rather than tempfile.gettempdir()

  This will result in better test isolation and automatic cleanup. (`#742 <https://github.com/dbfixtures/pytest-mongo/issues/742>`__)


Miscellaneus
------------

- Adjust workflows for actions-reuse 4.1.1 (`#690 <https://github.com/dbfixtures/pytest-mongo/issues/690>`__)
- Add release workflow to ease release process. (`#712 <https://github.com/dbfixtures/pytest-mongo/issues/712>`__)
- Add pre-commit hook to check Python version consistency in pyproject.toml. (`#714 <https://github.com/dbfixtures/pytest-mongo/issues/714>`__)
- Add architecture diagram to the README. (`#715 <https://github.com/dbfixtures/pytest-mongo/issues/715>`__)
- Add tests to check for support of minimum supported versions.

  Defined minimum supported versions at:

  * pytest - 7.0
  * port-for - 0.7.3
  * mirakuru - 2.6.0
  * pymongo - 4.10.0 (`#721 <https://github.com/dbfixtures/pytest-mongo/issues/721>`__)
- Run xdist tests on CI with -n auto. (`#723 <https://github.com/dbfixtures/pytest-mongo/issues/723>`__)
- Replace black with ruff-format.

  Should speed pre-commit up. (`#728 <https://github.com/dbfixtures/pytest-mongo/issues/728>`__)
- Update pytest configuration options to be toml native, as pytest 9 accepts native toml configuration.

  Created configuration for the tests with the oldest supported packages versions . (`#735 <https://github.com/dbfixtures/pytest-mongo/issues/735>`__)
- Add --no-mongo-tz-aware CLI flag and document tz-aware override behavior. (`#745 <https://github.com/dbfixtures/pytest-mongo/issues/745>`__)
- Add basic coderabbit configuration
- Drop MongoDB 6 from CI
- README clarifications and improvements.
- Separated factories into its own source files.


3.2.1 (2025-08-01)
==================

Bugfixes
--------

- Add missing py.typed file. (`#663 <https://github.com/dbfixtures/pytest-mongo/issues/663>`__)


3.2.0 (2025-02-28)
==================

Breaking changes
----------------

- Dropped Python 3.8 from CI and support


Features
--------

- Declare support for Python 3.13 (`#609 <https://github.com/dbfixtures/pytest-mongo/issues/609>`__)


Miscellaneus
------------

- Add MongoDB 8.0 support to CI
- Adjust links after repository transfer
- Adjust workflows for actions-reuse 3
- Pin OS to Ubuntu 22.04 for Mongo 7 and 6 tests.
- Use pre-commit for maintaining code style and linting


3.1.0 (2024-03-13)
==================

Features
--------

- Support Python 3.12 (`#507 <https://github.com/dbfixtures/pytest-mongo/issues/507>`__)


Miscellaneus
------------

- `#486 <https://github.com/dbfixtures/pytest-mongo/issues/486>`__, `#488 <https://github.com/dbfixtures/pytest-mongo/issues/488>`__, `#508 <https://github.com/dbfixtures/pytest-mongo/issues/508>`__


3.0.0 (2023-07-20)
==================

Breaking changes
----------------

- Dropped support for python 3.7 (`#384 <https://github.com/dbfixtures/pytest-mongo/issues/384>`__)


Features
--------

- Add typing and check types on CI (`#384 <https://github.com/dbfixtures/pytest-mongo/issues/384>`__)
- Officially support python 3.11 (`#385 <https://github.com/dbfixtures/pytest-mongo/issues/385>`__)


Miscellaneus
------------

- `#379 <https://github.com/dbfixtures/pytest-mongo/issues/379>`__, `#380 <https://github.com/dbfixtures/pytest-mongo/issues/380>`__, `#381 <https://github.com/dbfixtures/pytest-mongo/issues/381>`__, `#382 <https://github.com/dbfixtures/pytest-mongo/issues/382>`__, `#383 <https://github.com/dbfixtures/pytest-mongo/issues/383>`__, `#386 <https://github.com/dbfixtures/pytest-mongo/issues/386>`__, `#394 <https://github.com/dbfixtures/pytest-mongo/issues/394>`__, `#419 <https://github.com/dbfixtures/pytest-mongo/issues/419>`__


2.1.1
=====

Misc
----

- support only for python 3.7 and up
- rely on `get_port` functionality delivered by `port_for`


2.1.0
=====

- [feature] Add noproces fixture that can be used along the client to connect to
  already existing MongoDB instance.

2.0.0
=====

- [feature] Allow for mongo client to be configured with time zone awarness
- [feature] Drop support for python 2.7. From now on, only support python 3.6 and up

1.2.1
=====

- fix pypi description

1.2.0
=====

- [enhancement] require at least pymongo 3.6

1.1.2
=====

- [enhancement] removed path.py depdendency

1.1.1
=====

- [enhancements] set executor timeout to 60. By default mirakuru waits indefinitely, which might cause test hangs

1.1.0
=====

- [feature] - migrate usage of getfuncargvalue to getfixturevalue. require at least pytest 3.0.0

1.0.0
=====

- [feature] defaults logs dir to $TMPDIR by default
- [feature] run on random port by default (easier xdist integration)
- [feature] add command line and ini option for: executable, host, port, params and logsdir
