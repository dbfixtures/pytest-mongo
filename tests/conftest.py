"""Tests main conftest file."""

from pytest_mongo.factories import client, noprocess, process

# pylint:disable=invalid-name
mongo_params = "--noauth"

mongo_proc2 = process.mongo_proc(port=27070, params=mongo_params)
mongodb2 = client.mongodb("mongo_proc2", dbs=["test_db"])

mongo_proc3 = process.mongo_proc(port=27071, params=mongo_params)
mongodb3 = client.mongodb("mongo_proc3", dbs=["test_db"])

mongo_proc_rand = process.mongo_proc(port=None, params=mongo_params)
mongodb_rand = client.mongodb("mongo_proc_rand", dbs=["test_db"])

# Client fixture that declares the databases it manages, so its teardown drops
# only those and leaves everything else on the instance alone. Random port, so
# parallel workers get an instance each and never clean up after one another.
mongo_proc_dbs = process.mongo_proc(port=None, params=mongo_params)
mongodb_dbs = client.mongodb("mongo_proc_dbs", dbs=["pytest_mongo_managed"])

# Auth fixtures — mongo_proc_auth starts its own mongod with --auth and creates
# a root user via the localhost exception.
mongo_proc_auth = process.mongo_proc(username="testuser", password="testpass")
mongodb_proc_auth = client.mongodb("mongo_proc_auth", dbs=["test_db"])

# mongo_noproc_auth points at an externally running auth-enabled MongoDB.
# Tests that use mongodb_noproc_auth are guarded with skipif(MONGO_AUTH_ENABLED)
# so they only run when the CI provides such a service.
mongo_noproc_auth = noprocess.mongo_noproc(username="root", password="secret", auth_source="admin")
mongodb_noproc_auth = client.mongodb("mongo_noproc_auth", dbs=["test_db"])

# Same external MongoDB but addressed via a full URI (exercises the URI path).
mongo_noproc_uri = noprocess.mongo_noproc(
    uri="mongodb://root:secret@127.0.0.1:27017/?authSource=admin"
)
mongodb_noproc_uri = client.mongodb("mongo_noproc_uri", dbs=["test_db"])
# pylint:enable=invalid-name
