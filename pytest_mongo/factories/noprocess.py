"""Noprocess fixture factory for pytest-mongo."""

from typing import Callable, Iterator

import pytest
from _pytest.fixtures import FixtureRequest

from pytest_mongo.config import get_config
from pytest_mongo.executor_noop import MongoNoopExecutor


def mongo_noproc(
    host: str | None = None,
    port: int | None = None,
    username: str | None = None,
    password: str | None = None,
    auth_source: str | None = None,
    uri: str | None = None,
    tls: bool | None = None,
) -> Callable[[FixtureRequest], Iterator[MongoNoopExecutor]]:
    """MongoDB noprocess factory.

    :param host: hostname
    :param port: exact port (e.g. '8000', 8000)
    :param username: MongoDB username for authentication
    :param password: MongoDB password for authentication
    :param auth_source: MongoDB authentication database (authSource)
    :param uri: full MongoDB URI (takes precedence over host/port/credentials when set)
    :param tls: whether to enable TLS/SSL
    :returns: function which provides a MongoDB NoopExecutor fixture
    """

    @pytest.fixture(scope="session")
    def mongo_noproc_fixture(request: FixtureRequest) -> Iterator[MongoNoopExecutor]:
        """Noop Process fixture for MongoDB.

        :param FixtureRequest request: fixture request object
        :returns: tcp executor-like object
        """
        config = get_config(request)
        mongo_host = host or config.host
        mongo_port = port or config.port or 27017
        assert mongo_port

        noop_exec = MongoNoopExecutor(
            host=mongo_host,
            port=mongo_port,
            username=username if username is not None else config.username,
            password=password if password is not None else config.password,
            auth_source=auth_source if auth_source is not None else config.auth_source,
            uri=uri if uri is not None else config.uri,
            tls=tls if tls is not None else config.tls,
        )

        yield noop_exec

    return mongo_noproc_fixture
