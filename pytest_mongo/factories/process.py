"""Process fixture factory for pytest-mongo."""

from typing import Callable, Iterator

import pytest
from mirakuru import TCPExecutor
from port_for import PortType, get_port
from pytest import FixtureRequest, TempPathFactory

from pytest_mongo.config import get_config


def mongo_proc(
    executable: str | None = None,
    params: str | None = None,
    host: str | None = None,
    port: PortType | None = -1,
) -> Callable[[FixtureRequest, TempPathFactory], Iterator[TCPExecutor]]:
    """Mongo process fixture factory.

    .. note::
        `mongod <http://docs.mongodb.org/v2.2/reference/mongod/>`_

    :param executable: path to mongod
    :param params: params
    :param host: hostname
    :param port:
    :returns: function which makes a mongo process
    """

    @pytest.fixture(scope="session")
    def mongo_proc_fixture(
        request: FixtureRequest, tmp_path_factory: TempPathFactory
    ) -> Iterator[TCPExecutor]:
        """Mongodb process fixture.

        :param FixtureRequest request: fixture request object
        :rtype: mirakuru.TCPExecutor
        :returns: tcp executor
        """
        config = get_config(request)
        tmpdir = tmp_path_factory.mktemp(f"pytest-mongo-{request.fixturename}")

        mongo_exec = executable or config.exec
        mongo_params = params or config.params

        mongo_host = host or config.host
        assert mongo_host
        mongo_port = get_port(port) or get_port(config.port)
        assert mongo_port

        logfile_path = tmpdir / f"mongo.{mongo_port}.log"
        db_path = tmpdir / f"db-{mongo_port}"
        db_path.mkdir()

        mongo_executor = TCPExecutor(
            (
                f"{mongo_exec} --bind_ip {mongo_host} --port {mongo_port} "
                f"--dbpath {db_path} "
                f"--logpath {logfile_path} {mongo_params}"
            ),
            host=mongo_host,
            port=mongo_port,
            timeout=60,
        )
        with mongo_executor:
            yield mongo_executor

    return mongo_proc_fixture
