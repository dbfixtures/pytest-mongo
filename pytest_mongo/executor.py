"""MongoDB executors providing connection details for mongodb client."""

from typing import Any

from mirakuru import TCPExecutor
from pymongo import MongoClient


class MongoExecutor(TCPExecutor):
    """TCPExecutor extended with MongoDB connection and authentication attributes."""

    username: str | None
    password: str | None
    auth_source: str | None
    uri: str | None
    tls: bool

    def __init__(
        self,
        command: str | list[str] | tuple[str, ...],
        host: str,
        port: int,
        username: str | None = None,
        password: str | None = None,
        auth_source: str | None = None,
        uri: str | None = None,
        tls: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initialize TCPExecutor with MongoDB connection and authentication attributes."""
        self.username = username
        self.password = password
        self.auth_source = auth_source
        self.uri = uri
        self.tls = tls
        super().__init__(command, host, port, **kwargs)


class MongoNoopExecutor:  # pylint: disable=too-few-public-methods
    """Nooperator executor.

    This executor actually does nothing more than provide connection details
    for existing MongoDB server. I.E. one already started either on machine
    or with the use of containerisation like kubernetes or docker compose.
    """

    def __init__(
        self,
        host: str,
        port: int,
        username: str | None = None,
        password: str | None = None,
        auth_source: str | None = None,
        uri: str | None = None,
        tls: bool = False,
    ) -> None:
        """Initialize nooperator executor mock.

        :param host: MongoDB hostname
        :param port: MongoDB port
        :param username: MongoDB username for authentication
        :param password: MongoDB password for authentication
        :param auth_source: MongoDB authentication database (authSource)
        :param uri: full MongoDB URI (takes precedence over host/port/credentials when set)
        :param tls: whether to enable TLS/SSL
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.auth_source = auth_source
        self.uri = uri
        self.tls = tls
        self._version: str | None = None

    def _make_client(self) -> MongoClient:
        """Build a MongoClient using URI or host/port with optional auth."""
        if self.uri:
            return MongoClient(self.uri)
        return MongoClient(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            authSource=self.auth_source,
            tls=self.tls,
        )

    @property
    def version(self) -> str:
        """Get MongoDB's version."""
        if not self._version:
            client: MongoClient = self._make_client()
            server_info = client.server_info()
            self._version = server_info["version"]
        assert self._version
        return self._version
