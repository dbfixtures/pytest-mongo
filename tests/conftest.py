"""Tests main conftest file."""

from pytest_mongo.factories import client, noprocess, process

# pylint:disable=invalid-name
mongo_params = "--noauth"

mongo_proc2 = process.mongo_proc(port=27070, params=mongo_params)
mongodb2 = client.mongodb("mongo_proc2")

mongo_proc3 = process.mongo_proc(port=27071, params=mongo_params)
mongodb3 = client.mongodb("mongo_proc3")

mongo_proc_rand = process.mongo_proc(port=None, params=mongo_params)
mongodb_rand = client.mongodb("mongo_proc_rand")

# Auth fixtures — mongo_proc_auth starts its own mongod with --auth and creates
# a root user via the localhost exception.
mongo_proc_auth = process.mongo_proc(username="testuser", password="testpass")
mongodb_proc_auth = client.mongodb("mongo_proc_auth")

# mongo_noproc_auth points at an externally running auth-enabled MongoDB.
# Tests that use mongodb_noproc_auth are guarded with skipif(MONGO_AUTH_ENABLED)
# so they only run when the CI provides such a service.
mongo_noproc_auth = noprocess.mongo_noproc(username="root", password="secret", auth_source="admin")
mongodb_noproc_auth = client.mongodb("mongo_noproc_auth")

# Same external MongoDB but addressed via a full URI (exercises the URI path).
mongo_noproc_uri = noprocess.mongo_noproc(
    uri="mongodb://root:secret@127.0.0.1:27017/?authSource=admin"
)
mongodb_noproc_uri = client.mongodb("mongo_noproc_uri")
# pylint:enable=invalid-name
