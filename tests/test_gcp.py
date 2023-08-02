"""Testing GCP functions"""
import logging
from logging import config
from src.gcp import gcloud_auth, gcloud_read

config.fileConfig("logger.ini")


def test_auth():
    """Testing Google credential authentication"""
    data = gcloud_auth(log=logging)
    data.authenticate()

    assert len(data.bucket_names) != 0
