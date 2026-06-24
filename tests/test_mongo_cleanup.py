from pymongo import MongoClient


def test_clean_specified_databases(mongodb4: MongoClient) -> None:
    """Test if only specified databases are cleaned."""
    test_db = mongodb4["test_db"]
    test_db.test.insert_one({"test": "test"})
    test_db2 = mongodb4["test_db2"]
    test_db2.test.insert_one({"test": "test"})

    assert "test_db" in mongodb4.list_database_names()
    assert "test_db2" in mongodb4.list_database_names()


def test_clean_specified_databases_again(mongodb5: MongoClient) -> None:
    """Test if only specified databases are cleaned."""
    assert "test_db" not in mongodb5.list_database_names()
    assert "test_db2" in mongodb5.list_database_names()


def test_keep_specified_databases(mongodb5: MongoClient) -> None:
    """Test if only specified databases are kept."""
    assert "test_db" not in mongodb5.list_database_names()
    assert "test_db2" in mongodb5.list_database_names()
