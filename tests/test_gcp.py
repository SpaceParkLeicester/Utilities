"""Testing GCP functions"""
import logging
from logging import config
from src.gcp import gcloud_auth, gcloud_read

config.fileConfig("logger.ini")


def test_auth():
    """Testing Google credential authentication"""
    project_id = "kinetic-hydro"
    data = gcloud_auth(log=logging)
    data.authenticate(project_id=project_id)

    assert len(data.bucket_names) != 0


def test_read_geojson():
    """Testing to read GeoJSON data from cloud"""
    project_id = "kinetic-hydro"
    bucket_name = "rivers-kh"
    file_path = "data/outputs/uganda/grwl/vector/NA35.json"
    src = gcloud_read(log=logging, project_id=project_id)
    src.geojson(bucket_name=bucket_name, file_path=file_path)
    assert src.loaded_content is not None
