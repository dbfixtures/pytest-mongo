# -*- coding: utf-8 -*-
# Copyright (C) 2016 by Clearcode <http://clearcode.cc>
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
"""Pytest-mongo plugin definition."""

from tempfile import gettempdir

from pytest import Parser

from pytest_mongo import factories

# pylint:disable=invalid-name
_help_executable = "Path to MongoDB executable"
_help_logsdir = "Path to logs directory"
_help_params = "Additional MongoDB parameters"
_help_host = "Host at which MongoDB will accept connections"
_help_port = "Port at which MongoDB will accept connections"
_help_tz_aware = "Have mongo client timezone aware"


def pytest_addoption(parser: Parser) -> None:
    """Configure pytest-mongo configuration options."""
    parser.addini(name="mongo_exec", help=_help_executable, default="/usr/bin/mongod")

    parser.addini(name="mongo_params", help=_help_params, default="")

    parser.addini(name="mongo_logsdir", help=_help_logsdir, default=gettempdir())

    parser.addini(name="mongo_host", help=_help_host, default="127.0.0.1")

    parser.addini(
        name="mongo_port",
        help=_help_port,
        default=None,
    )

    parser.addini(
        name="mongo_tz_aware",
        help=_help_tz_aware,
        type="bool",
        default=False,
    )

    parser.addoption(
        "--mongo-exec",
        action="store",
        metavar="path",
        dest="mongo_exec",
        help=_help_executable,
    )

    parser.addoption("--mongo-params", action="store", dest="mongo_params", help=_help_params)

    parser.addoption(
        "--mongo-logsdir",
        action="store",
        metavar="path",
        dest="mongo_logsdir",
        help=_help_logsdir,
    )

    parser.addoption(
        "--mongo-host",
        action="store",
        dest="mongo_host",
        help=_help_host,
    )

    parser.addoption("--mongo-port", action="store", dest="mongo_port", help=_help_port)

    parser.addoption(
        "--mongo-tz-aware",
        action="store",
        dest="mongo_tz_aware",
        help=_help_tz_aware,
    )


mongo_proc = factories.mongo_proc()
mongo_noproc = factories.mongo_noproc()
mongodb = factories.mongodb("mongo_proc")
