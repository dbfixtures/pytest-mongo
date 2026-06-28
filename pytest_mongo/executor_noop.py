"""MongoDB Noop executor providing connection details for mongodb client."""

from pymongo import MongoClient

from pytest_mongo.mongoclient import make_mongo_client


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

    @property
    def version(self) -> str:
        """Get MongoDB's version."""
        if not self._version:
            client: MongoClient = make_mongo_client(
                self.host,
                self.port,
                uri=self.uri,
                username=self.username,
                password=self.password,
                auth_source=self.auth_source,
                tls=self.tls,
            )
            server_info = client.server_info()
            self._version = server_info["version"]
        assert self._version
        return self._version
