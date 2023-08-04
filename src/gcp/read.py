import os
from urllib.parse import urlparse

from google.cloud.storage import Client

from src.gcp import gcloud_auth


class gcloud_read(gcloud_auth):
    """Read the blob data"""

    def __init__(self, log: isinstance = None, bucket: str = None) -> None:
        r"""Defining variables

        Args:\n
            log: custom logger ini file.
            bucket: Name of the storage bucket.
        """
        self.bucket = bucket
        super().__init__(log)
        super().authenticate()

    @staticmethod
    def gcs_shape_files(
        storage_client: Client = None,
        bucket_path: str = None,
        file_name: str = None,
        extension: str = None,
    ):
        """Get the gcs shape file paths

        Args:
            bucket_path: gcs bucket path, eg: 'gs://bucket_name/path'.
            file_name: Name of the file.
            file_extension: Extension of the searching file

        Source:https://medium.com/towards-data-engineering/get-keys-inside-the-gcs-bucket-at-the-subfolder-level-python-a9c82ca52563 # noqa: E501
        """
        gcs_path = urlparse(bucket_path, allow_fragments=False)
        bucket_name, key = gcs_path.netloc, gcs_path.path.lstrip("/")
        blobs = storage_client.list_blobs(bucket_name, prefix=key)
        files = [file.name for file in blobs if file.name.endswith(extension)]
        files = [file for file in files if os.path.basename(file).split(".")[0] == file_name]
        return files[0]
