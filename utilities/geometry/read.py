"""Reading data with Loading animation"""
import logging
from typing import Dict

import fiona
import fsspec
import geopandas as gpd
import pandas as pd

from utilities.utils import Loader

logging.getLogger("fiona").setLevel(logging.WARNING)


def crs_convert(df: pd.DataFrame) -> pd.DataFrame:
    r"""Convert the CRS to 4326

    Args:\n
        df: A GeoPandas dataframe
    """
    df = df.to_crs(crs=32636)
    df = df.to_crs(crs=4326)
    return df


def geo_pandas(file_path: str = None) -> pd.DataFrame:
    r"""reading local file into a GeoPandas dataframe

    Args:\n
        file_path: Pat to the shape file.
    """
    loader = Loader(
        "Started reading the data into GeoPandas dataframe....",
        "Finished reading",
        0.05,  # noqa : E501
    ).start()
    df = gpd.read_file(file_path)
    df = crs_convert(df)
    loader.stop()
    return df


def geojson_to_geopandas(geo_json: Dict = None) -> pd.DataFrame:
    r"""Reading a Dict into Geopandas dataframe

    Args:\n
        geo_json: A Geo JSON dictionary
    """
    loader = Loader(
        "Started reading the data into GeoPandas dataframe....",
        "Finished reading",
        0.05,  # noqa : E501
    ).start()
    df = gpd.GeoDataFrame(geo_json)
    df = crs_convert(df)
    loader.stop()
    return df


def bytes_to_geopandas(gpd_bytes: bytes = None) -> pd.DataFrame:
    r"""Reading bytes into GeoPandas dataframe

    Args:\n
        gpd_bytes: Bytes data read from GCP or web.
    """
    loader = Loader(
        "Started reading the data into GeoPandas dataframe....",
        "Finished reading",
        0.05,  # noqa : E501
    ).start()
    with fiona.BytesCollection(gpd_bytes) as f:
        crs = f.crs
        df = gpd.GeoDataFrame(f, crs=crs)
        df = crs_convert(df)
    loader.stop()
    return df


def web_read_shape_file(url_path: str = None) -> pd.DataFrame:
    r"""Read Shape files from Web

    Args:\n
        url_path: Web path to the file
    """
    loader = Loader(
        "Started reading the data into GeoPandas dataframe....",
        "Finished reading",
        0.05,  # noqa : E501
    ).start()
    with fsspec.open(url_path) as file:
        df = gpd.read_file(file)
        df = crs_convert(df)
    loader.stop()
    return df
