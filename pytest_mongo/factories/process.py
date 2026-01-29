"""Process fixture factory for pytest-mongo."""

import os
from shutil import rmtree
from tempfile import gettempdir
from typing import Callable, Iterator

import pytest
from _pytest.fixtures import FixtureRequest
from mirakuru import TCPExecutor
from port_for import PortType, get_port

from pytest_mongo.config import get_config


def mongo_proc(
    executable: str | None = None,
    params: str | None = None,
    host: str | None = None,
    port: PortType | None = -1,
    logsdir: str | None = None,
) -> Callable[[FixtureRequest], Iterator[TCPExecutor]]:
    """Mongo process fixture factory.

    .. note::
        `mongod <http://docs.mongodb.org/v2.2/reference/mongod/>`_

    :param executable: path to mongod
    :param params: params
    :param host: hostname
    :param port:
    :param logsdir: path to store log files.
    :returns: function which makes a mongo process
    """

    @pytest.fixture(scope="session")
    def mongo_proc_fixture(request: FixtureRequest) -> Iterator[TCPExecutor]:
        """Mongodb process fixture.

        :param FixtureRequest request: fixture request object
        :rtype: mirakuru.TCPExecutor
        :returns: tcp executor
        """
        config = get_config(request)
        tmpdir = gettempdir()

        mongo_exec = executable or config.exec
        mongo_params = params or config.params

        mongo_host = host or config.host
        assert mongo_host
        mongo_port = get_port(port) or get_port(config.port)
        assert mongo_port

        mongo_logsdir = logsdir or config.logsdir
        mongo_logpath = os.path.join(mongo_logsdir, f"mongo.{mongo_port}.log")
        mongo_db_path = os.path.join(tmpdir, f"mongo.{mongo_port}")
        os.mkdir(mongo_db_path)

        mongo_executor = TCPExecutor(
            (
                f"{mongo_exec} --bind_ip {mongo_host} --port {mongo_port} "
                f"--dbpath {mongo_db_path} "
                f"--logpath {mongo_logpath} {mongo_params}"
            ),
            host=mongo_host,
            port=mongo_port,
            timeout=60,
        )
        with mongo_executor:
            yield mongo_executor
        if os.path.exists(mongo_db_path):
            rmtree(mongo_db_path)

    return mongo_proc_fixture
