"""Tests main conftest file."""

from pytest_mongo.factories import client, process
from pytest_mongo.plugin import *  # noqa: F403

# pylint:disable=invalid-name
mongo_params = "--noauth"

mongo_proc2 = process.mongo_proc(port=27070, params=mongo_params)
mongodb2 = client.mongodb("mongo_proc2")

mongo_proc3 = process.mongo_proc(port=27071, params=mongo_params)
mongodb3 = client.mongodb("mongo_proc3")

mongo_proc_rand = process.mongo_proc(port=None, params=mongo_params)
mongodb_rand = client.mongodb("mongo_proc_rand")
# pylint:enable=invalid-name
