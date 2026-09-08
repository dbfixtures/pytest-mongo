"""Client fixture factory for pytest-mongo."""

import warnings
from collections.abc import Callable, Iterator

import pytest
from _pytest.fixtures import FixtureRequest
from pymongo import MongoClient

from pytest_mongo.config import get_config
from pytest_mongo.mongoclient import make_mongo_client

#: MongoDB's own databases. pytest-mongo will never manage these.
RESERVED_DBS = frozenset({"admin", "config", "local"})

DBS_DEPRECATION = (
    "pytest-mongo dropped every database it found on this MongoDB instance. "
    "This behaviour is deprecated and will be removed in a future major release, "
    "because it interferes with databases the test session does not own - most "
    "notably when tests run in parallel against a shared server. Declare the "
    "databases the client fixture manages instead, with the `dbs` argument of the "
    "`mongodb` factory, the `--mongo-dbs` command line option or the `mongo_dbs` "
    "pytest.ini option; only those will then be dropped."
)


def _resolve_dbs(dbs: list[str] | None, config_dbs: list[str]) -> list[str]:
    """Resolve which databases a client fixture manages.

    The factory argument wins over the command line and pytest.ini values, which
    ``config_dbs`` has already collapsed into a single list. An empty result
    selects the deprecated "drop everything" teardown.

    :param dbs: databases passed to the ``mongodb`` factory
    :param config_dbs: databases from the command line or pytest.ini
    :raises ValueError: if a reserved MongoDB database was requested
    :returns: databases to drop on teardown, empty for the deprecated behaviour
    """
    resolved = list(dbs) if dbs else list(config_dbs)
    reserved = sorted(set(resolved) & RESERVED_DBS)
    if reserved:
        raise ValueError(
            f"pytest-mongo will not manage MongoDB's reserved databases: {', '.join(reserved)}. "
            "Remove them from the fixture's dbs."
        )
    return resolved


def _clean_databases(mongo_conn: MongoClient, dbs: list[str]) -> None:
    """Drop the databases managed by a client fixture.

    Declared databases are dropped whole. With nothing declared, fall back to the
    deprecated behaviour of emptying every database on the instance, leaving
    Mongo's own ``system.*`` collections alone.

    :param mongo_conn: connection to clean up through
    :param dbs: databases to drop, empty for the deprecated behaviour
    """
    if dbs:
        for db_name in dbs:
            mongo_conn.drop_database(db_name)
        return

    warnings.warn(DBS_DEPRECATION, DeprecationWarning, stacklevel=2)
    for db_name in mongo_conn.list_database_names():
        database = mongo_conn[db_name]
        for collection_name in database.list_collection_names():
            collection = database[collection_name]
            # Do not delete any of Mongo "system" collections
            if not collection.name.startswith("system."):
                collection.drop()


def mongodb(
    process_fixture_name: str,
    tz_aware: bool | None = None,
    dbs: list[str] | None = None,
) -> Callable[[FixtureRequest], Iterator[MongoClient]]:
    """Mongo database factory.

    :param str process_fixture_name: name of the process fixture
    :param bool tz_aware: whether the client to be timezone aware or not
    :param list dbs: databases this fixture manages, and the only ones it drops
        at the end of each test. Defaults to dropping every database found on the
        instance, which is deprecated.
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

        mongo_dbs = _resolve_dbs(dbs, config.dbs)

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

        _clean_databases(mongo_conn, mongo_dbs)
        mongo_conn.close()

    return mongodb_factory
