#!/usr/bin/python3
""" Test .get() and .count() methods
"""
import models.engine.utility as util
from models import storage

util.load_test_data(overwrite=True)
print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count("State")))

first_state_id = list(storage.all("State").values())[0].id
print("First state: {}".format(storage.get("State", first_state_id)))
