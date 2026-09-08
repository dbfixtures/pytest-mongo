"""Client fixture factory for pytest-mongo."""

from collections.abc import Callable, Iterator

import pytest
from _pytest.fixtures import FixtureRequest
from pymongo import MongoClient

from pytest_mongo._databases import clean_databases, validate_dbs
from pytest_mongo.config import get_config
from pytest_mongo.mongoclient import make_mongo_client


def mongodb(
    process_fixture_name: str,
    tz_aware: bool | None = None,
    dbname: str | None = None,
    dbs: list[str] | None = None,
) -> Callable[[FixtureRequest], Iterator[MongoClient]]:
    """Mongo database factory.

    :param str process_fixture_name: name of the process fixture
    :param bool tz_aware: whether the client to be timezone aware or not
    :param str dbname: database this fixture manages and empties at the end of
        each test, defaulting to the ``mongo_dbname`` setting
    :param list dbs: further databases to manage alongside ``dbname``, for tests
        that use more than one database through a single client. Optional.
    :rtype: func
    :returns: function which makes a connection to mongo
    """

    @pytest.fixture
    def mongodb_factory(request: FixtureRequest) -> Iterator[MongoClient]:
        """Client fixture for MongoDB.

        :param FixtureRequest request: fixture request object
        :rtype: pymongo.connection.Connection
        :returns: connection to mongo database
        """
        mongodb_process = request.getfixturevalue(process_fixture_name)
        config = get_config(request)
        mongo_tz_aware = False
        if tz_aware is not None:
            mongo_tz_aware = tz_aware
        elif config.tz_aware is not None and isinstance(config.tz_aware, bool):
            mongo_tz_aware = config.tz_aware

        main_database = dbname or config.dbname
        additional_databases = dbs or config.dbs

        mongo_dbs = [main_database, *additional_databases]
        validate_dbs(mongo_dbs)

        mongo_uri = getattr(mongodb_process, "uri", None)
        mongo_host = mongodb_process.host
        mongo_port = mongodb_process.port
        mongo_username = getattr(mongodb_process, "username", None)
        mongo_password = getattr(mongodb_process, "password", None)
        mongo_auth_source = getattr(mongodb_process, "auth_source", None)
        mongo_tls = getattr(mongodb_process, "tls", False)

        mongo_conn: MongoClient = make_mongo_client(
            mongo_host,
            mongo_port,
            uri=mongo_uri,
            username=mongo_username,
            password=mongo_password,
            auth_source=mongo_auth_source,
            tls=mongo_tls,
            tz_aware=mongo_tz_aware,
        )

        yield mongo_conn

        clean_databases(mongo_conn, mongo_dbs)
        mongo_conn.close()

    return mongodb_factory
