from src.utils import json_file
import os
import logging
from logging import config

config.fileConfig("logger.ini")


def test_kinetic_hydro():
    """Testing Kinetic Hydro JSON file"""
    key = "riveratlas"
    file_path = os.path.join("data", "kinetic_hydro.json")
    data = json_file(log=logging, file_path=file_path)
    url = data.key(name=key)
    assert url is not None
