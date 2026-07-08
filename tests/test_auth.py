"""Tests for MongoDB authentication support (mongo_proc and mongo_noproc)."""

import os

import pytest
from pymongo import MongoClient

# ── mongo_proc auth ───────────────────────────────────────────────────────────
# mongo_proc_auth starts its own mongod with --auth and creates a root user via
# the localhost exception.  Each xdist worker gets its own mongod, so these
# tests need no special grouping.


def test_mongo_proc_auth_connection(mongodb_proc_auth: MongoClient) -> None:
    """Authenticated client can write and read back data."""
    db = mongodb_proc_auth["test_db"]
    db.test.insert_one({"auth": "proc"})
    assert db.test.find_one({"auth": "proc"})["auth"] == "proc"  # type: ignore[index]


def test_mongo_proc_auth_credentials_on_executor(mongo_proc_auth) -> None:  # type: ignore[no-untyped-def]
    """Executor exposes the credentials that were passed to mongo_proc."""
    assert mongo_proc_auth.username == "testuser"
    assert mongo_proc_auth.password == "testpass"
    assert mongo_proc_auth.auth_source == "admin"


# ── mongo_noproc auth ─────────────────────────────────────────────────────────
# These tests require an externally running auth-enabled MongoDB.  They are
# skipped unless MONGO_AUTH_ENABLED is set (done by the tests-auth.yml workflow
# which provides a Docker service with authentication configured).
#
# All noproc-auth tests share the same external server, so they run in one
# xdist group to avoid parallel teardown interference between workers.

_needs_auth_service = pytest.mark.skipif(
    not os.environ.get("MONGO_AUTH_ENABLED"),
    reason="MONGO_AUTH_ENABLED not set – no auth-enabled MongoDB service available",
)


@_needs_auth_service
@pytest.mark.xdist_group("noproc_auth")
def test_mongo_noproc_auth_connection(mongodb_noproc_auth: MongoClient) -> None:
    """Authenticated noproc client can write and read back data."""
    db = mongodb_noproc_auth["test_db"]
    db.test.insert_one({"auth": "noproc"})
    assert db.test.find_one({"auth": "noproc"})["auth"] == "noproc"  # type: ignore[index]


@_needs_auth_service
@pytest.mark.xdist_group("noproc_auth")
def test_mongo_noproc_auth_credentials_on_executor(mongo_noproc_auth) -> None:  # type: ignore[no-untyped-def]
    """NoopExecutor exposes the credentials that were passed to mongo_noproc."""
    assert mongo_noproc_auth.username == "root"
    assert mongo_noproc_auth.password == "secret"
    assert mongo_noproc_auth.auth_source == "admin"


@_needs_auth_service
@pytest.mark.xdist_group("noproc_auth")
def test_mongo_noproc_uri_connection(mongodb_noproc_uri: MongoClient) -> None:
    """Full-URI noproc client can connect and perform basic operations."""
    db = mongodb_noproc_uri["test_db"]
    db.test.insert_one({"auth": "uri"})
    assert db.test.find_one({"auth": "uri"})["auth"] == "uri"  # type: ignore[index]
