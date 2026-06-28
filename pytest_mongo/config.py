"""Mongo config getter."""

from dataclasses import dataclass
from typing import Any

from pytest import FixtureRequest


@dataclass
class MongoConfig:
    """Mongo config dataclass."""

    exec: str
    host: str
    port: int | None
    port_search_count: int
    params: str
    tz_aware: bool
    username: str | None
    password: str | None
    auth_source: str | None
    uri: str | None
    tls: bool


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
        port_search_count=int(get_mongo_option("port_search_count")),
        params=get_mongo_option("params"),
        tz_aware=get_mongo_option("tz_aware"),
        username=get_mongo_option("username") or None,
        password=get_mongo_option("password") or None,
        auth_source=get_mongo_option("auth_source") or None,
        uri=get_mongo_option("uri") or None,
        tls=request.config.getoption("mongo_tls")
        if request.config.getoption("mongo_tls") is not None
        else bool(request.config.getini("mongo_tls")),
    )
    return cfg
