"""Client fixture factory for pytest-mongo."""

from typing import Callable, Iterator

import pytest
from _pytest.fixtures import FixtureRequest
from pymongo import MongoClient

from pytest_mongo.config import get_config


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

        mongo_host = mongodb_process.host
        mongo_port = mongodb_process.port

        mongo_conn: MongoClient = MongoClient(mongo_host, mongo_port, tz_aware=mongo_tz_aware)

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
