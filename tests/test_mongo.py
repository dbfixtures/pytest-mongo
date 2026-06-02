"""pytest-mongo tests collection."""

import pytest
from mirakuru import TCPExecutor
from pymongo import MongoClient


def test_mongo(mongodb: MongoClient) -> None:
    """Simple test for mongodb connection to the set up process."""
    test_data = {
        "test1": "test1",
    }

    database = mongodb["test_db"]
    database.test.insert_one(test_data)
    assert database.test.find_one()["test1"] == "test1"  # type: ignore


@pytest.mark.xdist_group(name="many_mongo")
def test_third_mongo(mongodb: MongoClient, mongodb2: MongoClient, mongodb3: MongoClient) -> None:
    """Test with everal mongo processes and connections."""
    test_data_one = {
        "test1": "test1",
    }
    database = mongodb["test_db"]
    database.test.insert_one(test_data_one)
    assert database.test.find_one()["test1"] == "test1"  # type: ignore

    test_data_two = {
        "test2": "test2",
    }
    database = mongodb2["test_db"]
    database.test.insert_one(test_data_two)
    assert database.test.find_one()["test2"] == "test2"  # type: ignore

    test_data_three = {
        "test3": "test3",
    }
    database = mongodb3["test_db"]
    database.test.insert_one(test_data_three)
    assert database.test.find_one()["test3"] == "test3"  # type: ignore


@pytest.mark.xdist_group(name="many_mongo")
def test_mongo_proc(
    mongo_proc: TCPExecutor, mongo_proc2: TCPExecutor, mongo_proc3: TCPExecutor
) -> None:
    """Several mongodb processes running."""
    assert mongo_proc.running() is True
    assert mongo_proc2.running() is True
    assert mongo_proc3.running() is True


def test_random_port(mongodb_rand: MongoClient) -> None:
    """Test if mongo fixture can be started on random port."""
    server_info = mongodb_rand.server_info()
    assert "ok" in server_info
    assert server_info["ok"] == 1.0

class TestCleanSpecifiedDatabases:
    """Test if only specified databases are cleaned."""

    def test_clean_specified_databases(self, mongodb4: MongoClient) -> None:
        """Test if only specified databases are cleaned."""
        test_db = mongodb4["test_db"]
        test_db.test.insert_one({"test": "test"})
        test_db2 = mongodb4["test_db2"]
        test_db2.test.insert_one({"test": "test"})

        assert "test_db" in mongodb4.list_database_names()
        assert "test_db2" in mongodb4.list_database_names()

    def test_clean_specified_databases_again(self, mongodb4: MongoClient) -> None:
        """Test if only specified databases are cleaned."""
        assert "test_db" not in mongodb4.list_database_names()
        assert "test_db2" in mongodb4.list_database_names()