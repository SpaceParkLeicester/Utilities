import json
import os

import geopandas as gpd
import pandas as pd
from google.api_core.exceptions import NotFound
from shapely.geometry import shape

from utilities.gcp import gcloud_auth
from utilities.utils import Loader


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

    def json_data(self, bucket_name: str = None, file_path: str = None):
        r"""Read JSON data into dictionary variable and geopandas dataframe

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
            self.bytes = self.blob.download_as_bytes()
            self.loaded_content = json.loads(self.contents)
            self.loading.stop()

            self.loading = Loader(
                f"Reading the contents of {self.file_name} as GeoPandas dataframe....", "Done", 0.05
            )
            self.feature_list = [features for _, features in self.loaded_content.items()]
            self.feature_list = [feature for feature in self.feature_list[1]]
            self.geometries = [shape(feature["geometry"]) for feature in self.feature_list]
            self.gdf = gpd.GeoDataFrame(
                data=self.feature_list, geometry=self.geometries, crs="EPSG:4326"
            )
            self.gdf_properties = pd.json_normalize(self.gdf["properties"])
            self.df = pd.concat([self.gdf_properties, self.gdf["geometry"]], axis=1)
            self.loading.stop()
            return self.df
        except NotFound as e:
            self.log.debug(f"Either bucket or the path to the file are not correct\n{e}")
            return None
