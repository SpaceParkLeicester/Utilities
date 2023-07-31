from urllib.parse import urlparse

from src.gcp import gcloud_auth


class gcloud_read(gcloud_auth):
    """Read the blob data"""

    def __init__(self, log: isinstance = None, project_id: str = None) -> None:
        super().__init__(log, project_id)
        super().authenticate()

    def list_all_items(self, bucket_file_path: str = None, file_extension: str = None) -> None:
        """Getting the bucket paths to the required file ending

        Args:
            bucket_file_path: gcs bucket path, eg: 'gs://bucket_name/path'
            file_extension: Extension of the searching file

        Source:https://medium.com/towards-data-engineering/get-keys-inside-the-gcs-bucket-at-the-subfolder-level-python-a9c82ca52563
        """
        gcs_path = urlparse(bucket_file_path, allow_fragments=False)
        bucket_name, key = gcs_path.netloc, gcs_path.path.lstrip("/")
        self.blobs = self.storage_client.list_blobs(bucket_name, prefix=key)
        self.files = [file.name for file in self.blobs if file.name.endswith(file_extension)]
