"""Helper for building MongoClient instances."""

from typing import Any

from pymongo import MongoClient


def make_mongo_client(
    host: str,
    port: int,
    uri: str | None = None,
    username: str | None = None,
    password: str | None = None,
    auth_source: str | None = None,
    tls: bool = False,
    **kwargs: Any,
) -> MongoClient:
    """Build a MongoClient using URI or host/port with optional auth.

    :param host: MongoDB hostname
    :param port: MongoDB port
    :param uri: full MongoDB URI (takes precedence over host/port/credentials when set)
    :param username: MongoDB username for authentication
    :param password: MongoDB password for authentication
    :param auth_source: MongoDB authentication database (authSource)
    :param tls: whether to enable TLS/SSL
    :param kwargs: additional keyword arguments passed to MongoClient
    """
    if uri:
        return MongoClient(uri, **kwargs)
    client_kwargs: dict[str, Any] = {"host": host, "port": port, "tls": tls, **kwargs}
    if username is not None:
        client_kwargs["username"] = username
    if password is not None:
        client_kwargs["password"] = password
    if auth_source is not None:
        client_kwargs["authSource"] = auth_source
    return MongoClient(**client_kwargs)
