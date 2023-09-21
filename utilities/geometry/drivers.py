"""Functions related to a vector data"""
import os
from geopandas.geodataframe import GeoDataFrame
import pandas as pd


class save_vector:
    """Shape file functions"""

    def __init__(
        self,
        log: isinstance = None,
        df: GeoDataFrame = None,
        save_folder: str = None,
        file_name: str = None,
    ) -> None:
        r"""Defining variables

        Args:\n
            log: Logger ini file.
            df: A GeoPandas dataframe.
            save_folder: A folder path to save file.
            file_name: Name of the file to be saved
        """
        self.log = log
        self.df = df
        self.save_folder = save_folder
        self.file_name = file_name

        # create the folder if it does not exists
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)

    @staticmethod
    def write_dataframe(
        log: isinstance = None,
        df: GeoDataFrame = None,
        driver: str = None,
        save_folder: str = None,
        file_name: str = None,
    ) -> None:
        r"""Write dataframe into specified format

        Args:\n
            log: Logger ini file.
            df: A GeoPandas dataframe.
            save_folder: A folder path to save file.
            file_name: Name of the file to be saved
        """
        extensions = {"ESRI Shapefile": "shp", "GeoJSON": "json"}
        file_path = os.path.join(save_folder, f"{file_name}.{extensions[driver]}")
        if f"{file_name}.{extensions[driver]}" not in os.listdir(save_folder):
            try:
                assert "geometry" in df.columns
            except AssertionError:
                log.debug("Given geopandas dataframe does not have geometry column")
            else:
                if not os.path.exists(file_path):
                    df.to_file(file_path, driver=driver)
                    log.info(f"Find the {driver} file below!")
                    log.info(f"{file_path}")
                else:
                    log.debug(f"{file_path} already exists")
        else:
            log.debug(f"{file_name}.{extensions[driver]} exists in the folder: {save_folder}")

    def esri_shapefile(self) -> None:
        r"""Write GeoPandas dataframe into a shape file"""

        self.write_dataframe(
            log=self.log,
            df=self.df,
            driver="ESRI Shapefile",
            save_folder=self.save_folder,
            file_name=self.file_name,
        )
        self.file_path = os.path.join(self.save_folder, f"{self.file_name}.shp")

    def geo_json(self) -> None:
        """Write Geopandas dataframe as a GeoJSON file"""

        self.write_dataframe(
            log=self.log,
            df=self.df,
            driver="GeoJSON",
            save_folder=self.save_folder,
            file_name=self.file_name,
        )
        self.file_path = os.path.join(self.save_folder, f"{self.file_name}.geojson")
