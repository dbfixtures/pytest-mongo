"""Internal helpers for the databases a client fixture manages."""

from pymongo import MongoClient

SYSTEM_DBS = frozenset({"admin", "config", "local"})


def validate_dbs(databases: list[str]) -> None:
    system = sorted(set(databases) & SYSTEM_DBS)
    if system:
        raise ValueError(
            f"pytest-mongo will not manage MongoDB's system databases: {', '.join(system)}. "
            "Remove them from the fixture's dbname and dbs."
        )


def clean_databases(mongo_conn: MongoClient, dbs: list[str]) -> None:
    """Empty the databases managed by a client fixture.

    :param mongo_conn: connection to clean up through
    :param dbs: databases to empty
    """
    for db_name in dbs:
        database = mongo_conn[db_name]
        for collection_name in database.list_collection_names():
            collection = database[collection_name]
            # Do not delete any of Mongo "system" collections
            if not collection.name.startswith("system."):
                collection.drop()
