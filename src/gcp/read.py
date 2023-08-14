import json
import os

from google.api_core.exceptions import NotFound

from src.gcp import gcloud_auth
from src.utils import Loader


class gcloud_read(gcloud_auth):
    """Read the blob data"""

    def __init__(self, log: isinstance = None, project_id: str = None) -> None:
        r"""Defining variables

        Args:\n
            log: custom logger ini file.
            project_id: GCP project ID.
        """
        super().__init__(log)
        super().authenticate(project_id)

    def geojson(self, bucket_name: str = None, file_path: str = None):
        r"""Read GeoJSON data into dictionary variable

        Args:\n
            bucket_name: Name of the bucket.
            file_path: Path to the file in the bucket.
        """
        try:
            self.file_name = os.path.basename(file_path).split(".")[0]
            self.bucket = self.client.get_bucket(bucket_name)
            self.blob = self.bucket.blob(file_path)
            self.loading = Loader(
                f"Loading the contents of {self.file_name} GeoJSON file...", "Done", 0.05
            ).start()
            self.contents = self.blob.download_as_string().decode("utf-8")
            self.loaded_content = json.loads(self.contents)
            self.loading.stop()
        except NotFound as e:
            self.log.debug(f"Either bucket or the path to the file are not correct\n{e}")
