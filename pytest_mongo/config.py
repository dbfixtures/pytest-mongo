"""Mongo config getter."""

from pathlib import Path
from typing import Any, TypedDict

from pytest import FixtureRequest


class MongoConfigDict(TypedDict):
    """Typed Config dictionary."""

    exec: str
    host: str
    port: int | None
    params: str
    logsdir: Path
    tz_aware: bool


def get_config(request: FixtureRequest) -> MongoConfigDict:
    """Return a dictionary with config options."""

    def get_mongo_option(option: str) -> Any:
        name = "mongo_" + option
        return request.config.getoption(name) or request.config.getini(name)

    port = get_mongo_option("port")
    return MongoConfigDict(
        exec=get_mongo_option("exec"),
        host=get_mongo_option("host"),
        port=int(port) if port else None,
        params=get_mongo_option("params"),
        logsdir=get_mongo_option("logsdir"),
        tz_aware=get_mongo_option("tz_aware"),
    )
