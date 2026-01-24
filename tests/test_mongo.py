"""pytest-mongo tests collection."""

import os

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


def test_third_mongo(
    mongodb: MongoClient, mongodb2: MongoClient, mongodb3: MongoClient
) -> None:
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


def test_mongo_proc(
    mongo_proc: TCPExecutor, mongo_proc2: TCPExecutor, mongo_proc3: TCPExecutor
) -> None:
    """Several mongodb processes running."""
    for mongo in (mongo_proc, mongo_proc2, mongo_proc3):
        assert os.path.isfile("/tmp/mongo.{port}.log".format(port=mongo.port))


def test_random_port(mongodb_rand: MongoClient) -> None:
    """Test if mongo fixture can be started on random port."""
    server_info = mongodb_rand.server_info()
    assert "ok" in server_info
    assert server_info["ok"] == 1.0
