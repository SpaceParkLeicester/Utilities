"""
UTM-Grid zones
Source: https://en.wikipedia.org/wiki/Universal_Transverse_Mercator_coordinate_system
"""
from typing import List

import numpy as np
import rasterio
from pyproj import transform


class utm_grid_zones:
    """Functions related to the UTM Grid zones"""

    def __init__(self, log: isinstance = None) -> None:
        r"""Defining variables

        Args:\n
            log: custom logger ini function.
        """
        self.log = log

    @staticmethod
    def raster_wgs84_bounds(src_raster_data: rasterio.DatasetReader = None) -> List:
        r"""Get the WGS84 coordinate bounds for a given raster geotiff through rasterio

        Args:\n
            src_raster_data: Read a GeoTIFF file with rasterio
        """
        bounds_native_crs = src_raster_data.bounds

        src_crs = src_raster_data.crs
        dst_crs = {"init": "epsg:4326"}

        # Transform the bounds to WGS84
        left_wgs84, bottom_wgs84 = transform(
            src_crs, dst_crs, bounds_native_crs.left, bounds_native_crs.bottom
        )
        right_wgs84, top_wgs84 = transform(
            src_crs, dst_crs, bounds_native_crs.right, bounds_native_crs.top
        )
        return [left_wgs84, bottom_wgs84, right_wgs84, top_wgs84]

    @staticmethod
    def equal_intervals_dividend(upper_limit, lower_limit, equal_interval: np.int16 = 5):
        r"""Get a divided of a range that can be divided into given equal intervals

        Args:\n
            upper_limit: Upper limit of a range, float or int
            lower_limit: Lower limit of a range, float or int
            equal_interval: Equal intervals of the range that is needed to be divided

        """
        return (upper_limit - lower_limit) / equal_interval

    @staticmethod
    def createZoneTable(
        log: isinstance = None, bounding_box_coords: List = None, intervals: np.int16 = 5
    ):
        r"""Creating an array of WGS84 coordinate zones

        Args:\n
            log: logging function.
            bounding_box_coords: A list of bounding box coords in the order below
                [left_wgs84, bottom_wgs84, right_wgs84, top_wgs84]
            intervals: Number of equal intervals or zones, if given
        """
        # Sanity checks
        try:
            left_wgs84, bottom_wgs84, right_wgs84, top_wgs84 = bounding_box_coords
            assert intervals < (right_wgs84 - left_wgs84)
            assert intervals < (top_wgs84 - bottom_wgs84)
        except AssertionError:
            log.debug("Please change the interval size to accommodate bounding box range")
            return None
        else:
            zone_table = list()
            longitudes = np.arange(left_wgs84, right_wgs84 + intervals, intervals)[:-1]
            latitudes = np.arange(bottom_wgs84, top_wgs84 + intervals, intervals)[:-1]

            for i in range(1, len(longitudes)):
                for j in range(1, len(latitudes)):
                    zone_table.append(
                        [
                            [
                                [latitudes[j - 1], longitudes[i - 1]],
                                [latitudes[j - 1], longitudes[i]],
                                [latitudes[j], longitudes[i]],
                                [latitudes[j], longitudes[i - 1]],
                                [latitudes[j - 1], longitudes[i - 1]],
                            ]
                        ]
                    )
            return zone_table

    @staticmethod
    def sanity_checks(grid_number: str = None) -> bool:
        r"""Perform sanity checks

        Args:\n
            grid_number: Provide a grid number with latitude and longitude and cardinal direction
                example: N00E33
        """
        # TODO: Perform sanity checks with grid numbers if it meets above example format
        # Return true or false
        pass

    @staticmethod
    def gird_tile_bounds(grid_number: str = None) -> List:
        r"""Get the geom bounds list with a grid tile number

        Args:\n
            grid_number: Provide a grid number with latitude and longitude and cardinal direction
                example: N00E33
        """
        # TODO: Convert gird tile numbers into a list of bound values (left, bottom, right, top)
        # Returns a list
        pass
