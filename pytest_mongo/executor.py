"""MongoDB executor providing connection details for mongodb client."""

from typing import Any, cast

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
        self._user_created = False
        super().__init__(command, host, port, **kwargs)

    def start(self: "MongoExecutor") -> "MongoExecutor":
        """Start the MongoDB executor and create the initial admin user if needed."""
        executor = cast(MongoExecutor, super().start())
        if self.username and self.password and self.auth_source and not self._user_created:
            try:
                self._create_mongo_user(
                    self.host, self.port, self.username, self.password, self.auth_source
                )
            except Exception:
                self.stop()
                raise
            self._user_created = True
        return executor

    def _create_mongo_user(
        self, host: str, port: int, username: str, password: str, auth_source: str
    ) -> None:
        """Create initial MongoDB user via the localhost exception.

        MongoDB permits one unauthenticated connection from localhost before any
        users exist, even when started with --auth. We use this to seed the first
        admin account so subsequent connections can authenticate normally.
        """
        client: MongoClient = MongoClient(host=host, port=port)
        try:
            client[auth_source].command(
                "createUser",
                username,
                pwd=password,
                roles=[{"role": "root", "db": auth_source}],
            )
        finally:
            client.close()
