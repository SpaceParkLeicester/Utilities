"""Testing GCP functions"""
import logging
from logging import config
from src.gcp import gcloud_auth

config.fileConfig("logger.ini")


def test_auth():
    """Testing Google credential authentication"""
    project_id = "kinetic-hydro"
    data = gcloud_auth(log=logging, project_id=project_id)
    data.authenticate()

    assert len(data.bucket_names) != 0
