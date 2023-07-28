"""Functions related to an ESRI Shapefile"""
import os

import pandas as pd


class shape_file:
    """Shape file functions"""

    def __init__(self, log: isinstance = None) -> None:
        r"""Defining variables

        Args:\n
            log: Logger ini file.
        """
        self.log = log

    def write(
        self, df: pd.DataFrame = None, save_folder: str = None, file_name: str = None
    ) -> None:
        r"""Write GeoPandas dataframe into a shape file

        Args:\n
            df: A GeoPandas dataframe.
            save_folder: Pat to the folder to save file.
            file_name: Name in which the file is saved.
        """
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        file_path = os.path.join(save_folder, f"{file_name}.shp")
        if f"{file_name}.shp" not in os.listdir(save_folder):
            try:
                assert "geometry" in df.columns
            except AssertionError:
                self.log.debug("Give geopandas dataframe does not have geometry column")
            else:
                if not os.path.exists(file_path):
                    df.to_file(file_path)
                    self.log.info("Find the written shape file below!")
                    self.log.info(f"{file_path}")
                else:
                    self.log.debug(f"Shape file {file_path} already exists")
        else:
            self.log.debug(f"{file_name}.shp exists in the folder: {save_folder}")
