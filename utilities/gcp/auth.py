"""Function to authenticate GCP account"""
from google.api_core.exceptions import BadRequest
from google.cloud import storage


class gcloud_auth:
    """Functions related to authentication"""

    def __init__(self, log: isinstance = None) -> None:
        """Initiating the variables

        Args:
            log: Custom logger file
        """
        self.log = log

    def authenticate(self, project_id: str = None):
        """Authenticate Google Cloud"""
        try:
            self.client = storage.Client(project=project_id)
            self.buckets = self.client.list_buckets()
            self.bucket_names = [bucket.name for bucket in self.buckets]
            self.log.info(f"List of buckets: {self.bucket_names}")
            self.log.info("Authentication successful")
        except BadRequest as b:
            self.log.debug("There was a problem with authentication")
            self.log.debug(f"{b}")
