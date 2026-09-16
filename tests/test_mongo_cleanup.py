"""Tests for the databases a client fixture manages and empties on teardown."""

import pytest
from pymongo import MongoClient

from pytest_mongo._databases import clean_databases, validate_dbs
from pytest_mongo.config import get_config


def _seed(mongo_conn: MongoClient, db_name: str) -> None:
    """Write a document so that MongoDB actually materialises the database."""
    mongo_conn[db_name].seed.insert_one({"seeded": db_name})


def test_default_dbname_is_test(request: pytest.FixtureRequest) -> None:
    """Without any configuration the fixture manages the ``test`` database."""
    assert get_config(request).dbname == "test"


def test_validate_dbs_accepts_ordinary_names() -> None:
    """Databases that are not MongoDB's own pass validation."""
    validate_dbs(["test", "orders", "customers"])


@pytest.mark.parametrize(
    ("dbs", "reported"),
    [
        (["admin"], "admin"),
        (["config"], "config"),
        (["local"], "local"),
        (["admin", "orders"], "admin"),
        (["config", "orders"], "config"),
        (["local", "orders"], "local"),
        (["admin", "orders", "local"], "admin, local"),
    ],
)
def test_validate_dbs_rejects_system_databases(dbs: list[str], reported: str) -> None:
    """MongoDB's own databases can never be managed, and the error names each one."""
    with pytest.raises(ValueError, match=f"system databases: {reported}\\."):
        validate_dbs(dbs)


def test_clean_empties_managed_databases_only(mongodb_dbs: MongoClient) -> None:
    """Managed databases are emptied, undeclared ones are left untouched."""
    _seed(mongodb_dbs, "pytest_mongo_main")
    _seed(mongodb_dbs, "pytest_mongo_extra")
    _seed(mongodb_dbs, "pytest_mongo_bystander")

    clean_databases(mongodb_dbs, ["pytest_mongo_main", "pytest_mongo_extra"])

    assert mongodb_dbs["pytest_mongo_main"].list_collection_names() == []
    assert mongodb_dbs["pytest_mongo_extra"].list_collection_names() == []
    assert mongodb_dbs["pytest_mongo_bystander"].list_collection_names() == ["seed"]

    # Nothing else will, so clean up what this test deliberately left behind.
    mongodb_dbs["pytest_mongo_bystander"].seed.drop()


def test_clean_leaves_system_collections_alone(mongodb_dbs: MongoClient) -> None:
    """Emptying a managed database does not touch Mongo's own collections."""
    _seed(mongodb_dbs, "pytest_mongo_main")
    managed = mongodb_dbs["pytest_mongo_main"]
    managed.command("create", "a_view", viewOn="seed", pipeline=[])

    clean_databases(mongodb_dbs, ["pytest_mongo_main"])

    # The view is a normal collection name and goes; system.views is left in place.
    assert managed.list_collection_names() == ["system.views"]


def test_clean_missing_database_is_a_noop(mongodb_dbs: MongoClient) -> None:
    """A managed database that was never written to is not an error."""
    clean_databases(mongodb_dbs, ["pytest_mongo_never_created"])

    assert mongodb_dbs["pytest_mongo_never_created"].list_collection_names() == []
