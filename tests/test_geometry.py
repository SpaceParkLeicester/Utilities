"""Test for geometry utility functions"""
import logging
from logging import config
import rasterio as rio
from utilities.geometry import utm_grid_zones, raster_clip

config.fileConfig("logger.ini")


def test_raster_data_grid_zones():
    """Testing raster image"""
    raster_data_path = "data/raster/elevation.tiff"
    with rio.open(raster_data_path) as src:
        utm = utm_grid_zones(log=logging)
        raster_bounds = utm.raster_wgs84_bounds(src_raster_data=src)
        src.close()
    assert raster_bounds is not None


def test_grid_zones():
    """Testing WGS84 grid zones"""
    bounds = [30.0, -100.0, 34.9, -95.0]
    utm = utm_grid_zones(log=logging)
    intervals = utm.equal_intervals_dividend(upper_limit=bounds[2], lower_limit=bounds[0])
    grid_zones = utm.createZoneTable(bounding_box_coords=bounds, intervals=intervals)
    assert len(grid_zones) is not None
