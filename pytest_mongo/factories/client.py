"""Client fixture factory for pytest-mongo."""

from typing import Callable, Iterator

import pytest
from _pytest.fixtures import FixtureRequest
from pymongo import MongoClient

from pytest_mongo.config import get_config
from pytest_mongo.mongoclient import make_mongo_client


def mongodb(
    process_fixture_name: str, tz_aware: bool | None = None
) -> Callable[[FixtureRequest], Iterator[MongoClient]]:
    """Mongo database factory.

    :param str process_fixture_name: name of the process fixture
    :param bool tz_aware: whether the client to be timezone aware or not
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

        for db_name in mongo_conn.list_database_names():
            database = mongo_conn[db_name]
            for collection_name in database.list_collection_names():
                collection = database[collection_name]
                # Do not delete any of Mongo "system" collections
                if not collection.name.startswith("system."):
                    collection.drop()
        mongo_conn.close()

    return mongodb_factory
