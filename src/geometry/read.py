"""Reading data with Loading animation"""
import geopandas as gpd
import pandas as pd

from src.utils import Loader


def geo_pandas(file_path: str = None) -> pd.DataFrame:
    r"""reading GeoPandas dataframe

    Args:\n
        file_path: Pat to the shape file.
    """
    loader = Loader(
        "Started reading the data into GeoPandas dataframe....", "Finished reading", 0.05
    ).start()  # noqa : E501
    df = gpd.read_file(file_path)
    df = df.to_crs(crs=32636)
    df = df.to_crs(crs=4326)
    loader.stop()
    return df
