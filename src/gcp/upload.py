"""Upload file to GCP bucket"""
import logging
import os
import shutil
import subprocess as sp
from logging import config

import click
from google.api_core.exceptions import NotFound

from src import gcloud_auth

config.fileConfig("logger.ini")


class GoogleBuckets(gcloud_auth):
    """Class function related to Google Buckets"""

    def __init__(
        self,
        log: isinstance = None,
        local_filepath: str = None,
        project_id: str = None,
        bucket_name: str = None,
        bucket_path: str = None,
    ) -> None:
        """Initiating Google Client

        Args:
            log: custom logger ini file.
            local_filepath: Relative path of the file needs to be uploaded.
            project_id: GCP project ID.
            bucket_name: Name of the bucket.
            bucket_path: bucket path of the file uploading.
            log: instance of custom logger function.
        """
        super().__init__(log)
        super().authenticate(project_id=project_id)
        self.log = log
        self.local_filepath = local_filepath
        self.bucket_path = bucket_path
        self.bucket_name = bucket_name

    def upload(self) -> None:
        """Uploading to the GCP buckets"""
        # Getting the filename
        self.filename = os.path.basename(self.local_filepath)
        self.abs_filepath = os.path.join(os.getcwd(), self.local_filepath)

        if os.path.exists(self.abs_filepath):
            # Listing files in the bucket
            self.bucket_name = self.bucket_path.split("/")[0]
            try:
                self.blobs = self.client.list_blobs(self.bucket_name)
                self.bucket_files = [blob.name.split("/")[-1] for blob in self.blobs]
            except NotFound:
                self.log(f"bucket{self.bucket_name} is not found in GCP")
            else:
                if self.filename not in self.bucket_files:
                    self.log.info(f"file {self.filename} not found in GCP")
                    self.log.info("Commencing upload!")
                    # Uploading file
                    sp.check_call(
                        f"gsutil cp -r {self.abs_filepath} gs://{self.bucket_name}/{self.bucket_path}",  # noqa : E501
                        shell=True,
                        stdout=sp.PIPE,
                    )
                    self.log.info("Upload finished")
                else:
                    self.log.debug(f"{self.filename} exists in GCP")
        else:
            self.log.debug(f"file {self.local_filepath} does not exist")

    def remove_uploaded_files(self) -> None:
        """Removing files from local system"""
        # Removing file
        if os.path.exists(self.abs_filepath):
            shutil.rmtree(self.abs_filepath, ignore_errors=True)
        else:
            self.log.debug(f"file {self.abs_filepath} does not exist")


@click.command()
@click.option("--file_path", help="Relative path to the file.")
@click.option("--bucket_path", help="Bucket Path without 'gs://bucket_name")
@click.option("--bucket_name", help="Name of the bucket.")
def main(file_path, bucket_path, bucket_name):
    """Main function"""
    src = GoogleBuckets(
        local_filepath=file_path, bucket_path=bucket_path, bucket_name=bucket_name, log=logging
    )
    src.upload()
    src.remove_uploaded_files()


if __name__ == "__main__":
    main()
