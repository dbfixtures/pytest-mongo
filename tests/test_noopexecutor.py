"""Test for NoopExecutor."""

from mirakuru import TCPExecutor
from pymongo import MongoClient

from pytest_mongo.executor_noop import NoopExecutor


def test_nooproc_version(mongo_proc: TCPExecutor) -> None:
    """Test the way mongo version is being read."""
    mongo_nooproc = NoopExecutor(mongo_proc.host, mongo_proc.port)
    proc_client: MongoClient = MongoClient(host=mongo_proc.host, port=mongo_proc.port)
    assert proc_client.server_info()["version"] == mongo_nooproc.version


def test_nooproc_cached_version(mongo_proc: TCPExecutor) -> None:
    """Test that the version is being cached."""
    mongo_nooproc = NoopExecutor(mongo_proc.host, mongo_proc.port)
    ver = mongo_nooproc.version

    with mongo_proc.stopped():
        assert ver == mongo_nooproc.version
