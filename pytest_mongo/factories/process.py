"""Process fixture factory for pytest-mongo."""

from typing import Callable, Iterable, Iterator

import pytest
from port_for import PortForException, PortType, get_port
from pytest import FixtureRequest, TempPathFactory

from pytest_mongo.config import MongoConfig, get_config
from pytest_mongo.executor import MongoExecutor


def _mongo_port(port: PortType | None, config: MongoConfig, excluded_ports: Iterable[int]) -> int:
    """User specified port, otherwise find an unused port from config."""
    mongo_port = get_port(port, excluded_ports) or get_port(config.port, excluded_ports)
    assert mongo_port is not None
    return mongo_port


def mongo_proc(
    executable: str | None = None,
    params: str | None = None,
    host: str | None = None,
    port: PortType | None = -1,
    username: str | None = None,
    password: str | None = None,
    auth_source: str | None = None,
) -> Callable[[FixtureRequest, TempPathFactory], Iterator[MongoExecutor]]:
    """Mongo process fixture factory.

    .. note::
        `mongod <http://docs.mongodb.org/v2.2/reference/mongod/>`_

    :param executable: path to mongod
    :param params: params
    :param host: hostname
    :param port:
    :param username: if set, mongod is started with ``--auth`` and this user is
        created via the localhost exception; subsequent connections authenticate
        with this account
    :param password: password for the admin user (required when username is set)
    :param auth_source: authentication database, defaults to ``"admin"``
    :returns: function which makes a mongo process
    """

    @pytest.fixture(scope="session")
    def mongo_proc_fixture(
        request: FixtureRequest, tmp_path_factory: TempPathFactory
    ) -> Iterator[MongoExecutor]:
        """Mongodb process fixture.

        :param FixtureRequest request: fixture request object
        :rtype: mirakuru.TCPExecutor
        :returns: tcp executor
        """
        config = get_config(request)
        tmpdir = tmp_path_factory.mktemp(f"pytest-mongo-{request.fixturename}")

        port_path = tmp_path_factory.getbasetemp()
        if hasattr(request.config, "workerinput"):
            port_path = tmp_path_factory.getbasetemp().parent

        n = 0
        used_ports: set[int] = set()
        while True:
            try:
                mongo_port = _mongo_port(port, config, used_ports)
                port_filename_path = port_path / f"mongo-{mongo_port}.port"
                if mongo_port in used_ports:
                    raise PortForException(
                        f"Port {mongo_port} already in use, "
                        f"probably by other instances of the test. "
                        f"{port_filename_path} is already used."
                    )
                used_ports.add(mongo_port)
                with (port_filename_path).open("x") as port_file:
                    port_file.write(f"mongo_port {mongo_port}\n")
                break
            except FileExistsError:
                n += 1
                if n >= config.port_search_count:
                    raise PortForException(
                        f"Attempted {n} times to select ports. "
                        f"All attempted ports: {', '.join(map(str, used_ports))} are already "
                        f"in use, probably by other instances of the test."
                    ) from None

        mongo_exec = executable or config.exec
        mongo_params = params or config.params

        mongo_host = host or config.host
        assert mongo_host

        mongo_username = username if username is not None else config.username
        mongo_password = password if password is not None else config.password
        mongo_auth_source = (
            auth_source if auth_source is not None else config.auth_source
        ) or "admin"

        auth_flag = "--auth" if mongo_username else ""

        logfile_path = tmpdir / f"mongo.{mongo_port}.log"
        db_path = tmpdir / f"db-{mongo_port}"
        db_path.mkdir()

        mongo_executor = MongoExecutor(
            command=(
                f"{mongo_exec} --bind_ip {mongo_host} --port {mongo_port} "
                f"--dbpath {db_path} "
                f"--logpath {logfile_path} {mongo_params} {auth_flag}".strip()
            ),
            host=mongo_host,
            port=mongo_port,
            username=mongo_username or None,
            password=mongo_password or None,
            auth_source=mongo_auth_source if mongo_username else None,
            uri=None,
            tls=False,
            timeout=60,
        )
        with mongo_executor:
            yield mongo_executor

    return mongo_proc_fixture
