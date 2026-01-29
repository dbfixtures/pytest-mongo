"""Mongo config getter."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pytest import FixtureRequest


@dataclass
class MongoConfig:
    """Mongo config dataclass."""

    exec: str
    host: str
    port: int | None
    params: str
    logsdir: Path
    tz_aware: bool


def get_config(request: FixtureRequest) -> MongoConfig:
    """Return a MongoConfig with config options."""

    def get_mongo_option(option: str) -> Any:
        name = "mongo_" + option
        return request.config.getoption(name) or request.config.getini(name)

    port = get_mongo_option("port")

    cfg = MongoConfig(
        exec=get_mongo_option("exec"),
        host=get_mongo_option("host"),
        port=int(port) if port else None,
        params=get_mongo_option("params"),
        logsdir=Path(get_mongo_option("logsdir")),
        tz_aware=get_mongo_option("tz_aware"),
    )
    return cfg
