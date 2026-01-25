# Copyright (C) 2013 by Clearcode <http://clearcode.cc>
# and associates (see AUTHORS).

# This file is part of pytest-mongo.

# pytest-mongo is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pytest-mongo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with pytest-mongo.  If not, see <http://www.gnu.org/licenses/>.
"""Fixture factories."""

import os
from shutil import rmtree
from tempfile import gettempdir
from typing import Callable, Iterator

import pytest
from mirakuru import TCPExecutor
from port_for import get_port
from port_for.api import PortType
from pymongo import MongoClient
from pytest import FixtureRequest

from pytest_mongo.config import get_config
from pytest_mongo.executor_noop import NoopExecutor


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

        mongo_exec = executable or config["exec"]
        mongo_params = params or config["params"]

        mongo_host = host or config["host"]
        assert mongo_host
        mongo_port = get_port(port) or get_port(config["port"])
        assert mongo_port

        mongo_logsdir = logsdir or config["logsdir"]
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
        os.path.exists(mongo_db_path)
        rmtree(mongo_db_path)

    return mongo_proc_fixture


def mongo_noproc(
    host: str | None = None, port: int | None = None
) -> Callable[[FixtureRequest], Iterator[NoopExecutor]]:
    """MongoDB noprocess factory.

    :param host: hostname
    :param port: exact port (e.g. '8000', 8000)
    :param user: MongoDB username
    :param password: MongoDB password
    :param options: MongoDB connection options
    :returns: function which makes a postgresql process
    """

    @pytest.fixture(scope="session")
    def mongo_noproc_fixture(request: FixtureRequest) -> Iterator[NoopExecutor]:
        """Noop Process fixture for MongoDB.

        :param FixtureRequest request: fixture request object
        :returns: tcp executor-like object
        """
        config = get_config(request)
        mongo_host = host or config["host"]
        mongo_port = port or config["port"] or 27017
        assert mongo_port

        noop_exec = NoopExecutor(host=mongo_host, port=mongo_port)

        yield noop_exec

    return mongo_noproc_fixture


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
        elif config["tz_aware"] is not None and isinstance(
            config["tz_aware"], bool
        ):
            mongo_tz_aware = config["tz_aware"]

        mongo_host = mongodb_process.host
        mongo_port = mongodb_process.port

        mongo_conn: MongoClient = MongoClient(
            mongo_host, mongo_port, tz_aware=mongo_tz_aware
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


__all__ = ("mongodb", "mongo_proc", "mongo_noproc")
