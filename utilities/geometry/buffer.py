"""Create a buffer for a vector file and clip another vectors inside the buffer"""
import logging

import geopandas as gpd
import numpy as np
import pandas as pd

logging.getLogger("fiona").setLevel(logging.WARNING)


class clip_vector:
    """Clip vectors with a buffer"""

    def __init__(self, log: isinstance = None) -> None:
        r"""Defining variables

        Args:\n
            log: Custom logger ini file.
        """
        self.log = log

    @staticmethod
    def create_buffer(
        buffer_df: pd.DataFrame = None, buffer_length: np.int32 = None
    ) -> pd.DataFrame:
        r"""Create a buffer around a vector layer

        Args:\n
            buffer_df: A GeoPandas dataframe for buffering.
            buffer_length: Length of a buffer in meters
        """
        try:
            assert "geometry" in buffer_df.columns
            buffer_df = buffer_df.to_crs(crs=32636)
            buffer_df["geometry"] = buffer_df.geometry.buffer(buffer_length)
            buffer_df = buffer_df.to_crs(crs=4326)
            return buffer_df
        except AssertionError:
            logging.debug("Give dataframe does not have a geometry column")
            return None

    def clip(
        self,
        clipping_df: pd.DataFrame = None,
        buffer_df: pd.DataFrame = None,
        buffer_length: np.int32 = None,
    ) -> pd.DataFrame:
        r"""Clip a vector layer with a another vector by a buffer

        Args:\n
            clipping_df: A vector layer that needs to be clipped.
            buffer_df: A vector layer around which the clipping does
            buffer_length: Length of buffer in meters.
        """
        self.buffer_df = self.create_buffer(buffer_df=buffer_df, buffer_length=buffer_length)
        try:
            assert self.buffer_df.crs == clipping_df.crs
            self.clipped_df = gpd.clip(clipping_df, self.buffer_df)
            return self.clipped_df
        except AssertionError:
            self.log.debug("Buffer dataframe and Clipping dataframe are not in the same CRS.")
            return None
