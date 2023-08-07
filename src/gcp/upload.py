"""Upload file to GCP bucket"""
import logging
import os
import subprocess as sp
from logging import config

import click
from google.api_core.exceptions import NotFound

from src.gcp import gcloud_auth

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

    def upload_files(self, local_folder_path: str = None, format: str = None) -> None:
        r"""Upload multiple files

        Args:\n
            format: Select a format that needs to be only uploaded. eg: 'json'
            local_folder_path: Local folder path of the files.
        """
        files_list = os.listdir(local_folder_path)
        if format is not None:
            selected_files = [
                file for file in files_list if os.path.basename(file).split(".")[1] == format
            ]  # noqa = E501
            file_paths = [os.path.join(local_folder_path, file) for file in selected_files]
        else:
            file_paths = [os.path.join(local_folder_path, file) for file in files_list]

        for file in file_paths:
            abs_file_path = os.path.join(os.getcwd(), file)
            if os.path.exists(file):
                try:
                    self.blobs = self.client.list_blobs(self.bucket_name)
                    self.bucket_files = [blob.name.split("/")[-1] for blob in self.blobs]
                except NotFound:
                    self.log(f"bucket{self.bucket_name} is not found in GCP")
                else:
                    if file not in self.bucket_files:
                        self.log.info(f"file {file} not found in GCP")
                        self.log.info("Commencing upload!")
                        # Uploading file
                        sp.check_call(
                            f"gsutil cp -r {abs_file_path} gs://{self.bucket_name}/{file}",  # noqa : E501
                            shell=True,
                            stdout=sp.PIPE,
                        )
                        self.log.info("Upload finished")
                    else:
                        self.log.debug(f"{file} exists in GCP")
            else:
                self.log.debug(f"file {file} does not exist")


@click.command()
@click.option("--project_id", help="GCP Project ID")
@click.option("--bucket", help="Name of the bucket.")
@click.option("--file_format", help="Format of the files that needs to be uploaded.")
@click.option("--local_folder", help="Path to the local folder.")
def main(project_id, bucket, local_folder, file_format):
    """Main function"""
    src = GoogleBuckets(project_id=project_id, bucket_name=bucket, log=logging)
    src.upload_files(format=file_format, local_folder_path=local_folder)


if __name__ == "__main__":
    main()
