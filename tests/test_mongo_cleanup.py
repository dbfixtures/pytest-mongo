"""Tests for the databases a client fixture manages and drops on teardown."""

import pytest
from pymongo import MongoClient

from pytest_mongo.factories.client import DBS_DEPRECATION, _clean_databases, _resolve_dbs


def _seed(mongo_conn: MongoClient, db_name: str) -> None:
    """Write a document so that MongoDB actually materialises the database."""
    mongo_conn[db_name].seed.insert_one({"seeded": db_name})


def test_resolve_dbs_prefers_factory_argument() -> None:
    """The factory argument wins over the command line and pytest.ini."""
    assert _resolve_dbs(["from_arg"], ["from_config"]) == ["from_arg"]


def test_resolve_dbs_falls_back_to_config() -> None:
    """Without a factory argument, the command line or pytest.ini value is used."""
    assert _resolve_dbs(None, ["from_config"]) == ["from_config"]
    assert _resolve_dbs([], ["from_config"]) == ["from_config"]


def test_resolve_dbs_empty_selects_deprecated_behaviour() -> None:
    """Declaring nothing anywhere leaves the deprecated drop-everything teardown."""
    assert _resolve_dbs(None, []) == []


@pytest.mark.parametrize("reserved", ["admin", "config", "local"])
def test_resolve_dbs_rejects_reserved_databases(reserved: str) -> None:
    """MongoDB's own databases can never be managed, whichever source names them."""
    with pytest.raises(ValueError, match="reserved databases"):
        _resolve_dbs([reserved], [])
    with pytest.raises(ValueError, match="reserved databases"):
        _resolve_dbs(None, [reserved])


def test_clean_drops_declared_databases_only(mongodb_dbs: MongoClient) -> None:
    """Declared databases are dropped, undeclared ones are left untouched."""
    _seed(mongodb_dbs, "pytest_mongo_managed")
    _seed(mongodb_dbs, "pytest_mongo_bystander")

    _clean_databases(mongodb_dbs, ["pytest_mongo_managed"])

    remaining = mongodb_dbs.list_database_names()
    assert "pytest_mongo_managed" not in remaining
    assert "pytest_mongo_bystander" in remaining

    # Nothing else will, so drop the database this test deliberately left behind.
    mongodb_dbs.drop_database("pytest_mongo_bystander")


def test_clean_missing_database_is_a_noop(mongodb_dbs: MongoClient) -> None:
    """A declared database that was never written to is not an error."""
    _clean_databases(mongodb_dbs, ["pytest_mongo_never_created"])

    assert "pytest_mongo_never_created" not in mongodb_dbs.list_database_names()


def test_clean_without_declared_databases_warns(mongodb_dbs: MongoClient) -> None:
    """With nothing declared, every database is emptied and a deprecation is raised."""
    _seed(mongodb_dbs, "pytest_mongo_legacy")

    with pytest.warns(DeprecationWarning) as records:
        _clean_databases(mongodb_dbs, [])

    assert str(records[0].message) == DBS_DEPRECATION
    assert "pytest_mongo_legacy" not in mongodb_dbs.list_database_names()
