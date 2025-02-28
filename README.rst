.. image:: https://raw.githubusercontent.com/dbfixtures/pytest-mongo/master/logo.png
    :width: 100px
    :height: 100px

pytest-mongo
============

.. image:: https://img.shields.io/pypi/v/pytest-mongo.svg
    :target: https://pypi.python.org/pypi/pytest-mongo/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/wheel/pytest-mongo.svg
    :target: https://pypi.python.org/pypi/pytest-mongo/
    :alt: Wheel Status

.. image:: https://img.shields.io/pypi/pyversions/pytest-mongo.svg
    :target: https://pypi.python.org/pypi/pytest-mongo/
    :alt: Supported Python Versions

.. image:: https://img.shields.io/pypi/l/pytest-mongo.svg
    :target: https://pypi.python.org/pypi/pytest-mongo/
    :alt: License


What is this?
=============

This is a pytest plugin, that enables you to test your code that relies on a running MongoDB database.
It allows you to specify fixtures for MongoDB process and client.

How to use
==========

Plugin contains two fixtures

* **mongodb** - it's a client fixture that has functional scope, and which cleans MongoDB at the end of each test.
* **mongo_proc** - session scoped fixture, that starts MongoDB instance at the first use and stops at the end of the tests.
* **mongo_noproc** - a no process fixture, that's connecting to already
  running mongodb instance.
  For example on dockerized test environments, or CI providing mongodb services

Simply include one of these fixtures into your tests fixture list.

You can also create additional MongoDB client and process fixtures if you'd need to:


.. code-block:: python

    from pytest_mongo import factories

    mongo_my_proc = factories.mongo_proc(
        port=None, logsdir='/tmp')
    mongo_my = factories.mongodb('mongo_my_proc')

.. note::

    Each MongoDB process fixture can be configured in a different way than the others through the fixture factory arguments.


Connecting to already existing mongodb database
-----------------------------------------------

Some projects are using already running MongoDB servers (ie on docker instances).
In order to connect to them, one would be using the ``mongo_noproc`` fixture.

.. code-block:: python

    mongo_external = factories.mongodb('mongo_noproc')

By default the  ``mongo_noproc`` fixture would connect to MongoDB instance using **27017** port. Standard configuration options apply to it.

These are the configuration options that are working on all levels with the ``mongo_noproc`` fixture:

Configuration
=============

You can define your settings in three ways, it's fixture factory argument, command line option and pytest.ini configuration option.
You can pick which you prefer, but remember that these settings are handled in the following order:

    * ``Fixture factory argument``
    * ``Command line option``
    * ``Configuration option in your pytest.ini file``

.. list-table:: Configuration options
   :header-rows: 1

   * - MongoDB server option
     - Fixture factory argument
     - Command line option
     - pytest.ini option
     - Noop process fixture
     - Default
   * - Path to mongodb exec
     - executable
     - --mongo-exec
     - mongo_exec
     - no
     - /usr/bin/mongod
   * - MongoDB host
     - host
     - --mongo-host
     - mongo_host
     - 127.0.0.1
     - 127.0.0.1
   * - MongoDB port
     - port
     - --mongo-port
     - port
     - 27017
     - random
   * - Path to store logs
     - logsdir
     - --mongo-logsdir
     - mongo_logsdir
     - no
     - $TMPDIR
   * - Additional parameters
     - params
     - --mongo-params
     - mongo_params
     - no
     -
   * - MongoDB client's time zone awarness
     - tz_aware
     - --mongo-tz-aware
     - mongo_tz_aware
     - no
     - False


Example usage:

* pass it as an argument in your own fixture

    .. code-block:: python

        mongo_proc = factories.mongo_proc(port=8888)

* use ``--mongo-port`` command line option when you run your tests

    .. code-block:: sh

        py.test tests --mongo-port=8888


* specify your directory as ``mongo_port`` in your ``pytest.ini`` file.

    To do so, put a line like the following under the ``[pytest]`` section of your ``pytest.ini``:

    .. code-block:: ini

        [pytest]
        mongo_port = 8888

Package resources
-----------------

* Bug tracker: https://github.com/dbfixtures/pytest-mongo/issues
