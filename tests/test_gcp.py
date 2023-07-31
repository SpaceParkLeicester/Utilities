"""Testing GCP functions"""
import logging
from logging import config
from src.gcp import gcloud_auth, gcloud_read

config.fileConfig("logger.ini")


def test_auth():
    """Testing Google credential authentication"""
    project_id = "kinetic-hydro"
    data = gcloud_auth(log=logging, project_id=project_id)
    data.authenticate()

    assert len(data.bucket_names) != 0


def test_bucket_read():
    """Reading the contents in the bucket"""
    project_id = "kinetic-hydro"
    bucket_name = "kinetic-hydro"
    file_path = "GRWL/uganda/vector/NA35.shp"
    gcp = gcloud_read(log=logging, project_id=project_id)
    gcp.shape_file(bucket_name=bucket_name, file_path=file_path)
    print(gcp.data)
