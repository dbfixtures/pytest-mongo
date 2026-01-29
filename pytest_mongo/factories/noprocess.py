"""Noprocess fixture factory for pytest-mongo."""

from typing import Callable, Iterator

import pytest
from _pytest.fixtures import FixtureRequest

from pytest_mongo.config import get_config
from pytest_mongo.executor_noop import NoopExecutor


def mongo_noproc(
    host: str | None = None, port: int | None = None
) -> Callable[[FixtureRequest], Iterator[NoopExecutor]]:
    """MongoDB noprocess factory.

    :param host: hostname
    :param port: exact port (e.g. '8000', 8000)
    :returns: function which provides a MongoDB NoopExecutor fixture
    """

    @pytest.fixture(scope="session")
    def mongo_noproc_fixture(request: FixtureRequest) -> Iterator[NoopExecutor]:
        """Noop Process fixture for MongoDB.

        :param FixtureRequest request: fixture request object
        :returns: tcp executor-like object
        """
        config = get_config(request)
        mongo_host = host or config.host
        mongo_port = port or config.port or 27017
        assert mongo_port

        noop_exec = NoopExecutor(host=mongo_host, port=mongo_port)

        yield noop_exec

    return mongo_noproc_fixture
