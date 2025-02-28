CHANGELOG
=========

.. towncrier release notes start

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
