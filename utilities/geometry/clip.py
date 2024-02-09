"""
Function to clip a raster and vector layer with coordinates extent, and other ways!
"""

import json
import os
from math import sqrt

import geojson
import geopandas as gpd
import numpy as np
import rasterio as rio
from rasterio.mask import mask
from shapely.geometry import mapping, shape
from shapely.wkt import loads

from osgeo import gdal

class raster_clip:
    """Function to clip the raster data"""

    def __init__(self, log: isinstance = None, raster_file: str = None) -> None:
        r"""Defining variables

        Args:\n
            log: custom logger ini file
            raster_file: Path to the raster file.
        """
        self.log = log
        self.raster_file = raster_file

    def bbox_geom_center(
        self, center_lat: np.uint64 = None, center_lon: np.uint64 = None, half_side: np.int16 = 10
    ):  # Km
        """Bounding box for a given coordinates pair"""
        # Sanity check
        assert half_side > 0
        assert center_lat >= -90.0 and center_lat <= 90.0
        assert center_lon >= -180.0 and center_lon <= 180.0

        # Km to m
        half_side = (half_side * 1000) / sqrt(2)

        # Geopandas geo-series
        gs = gpd.GeoSeries(loads(f"POINT({center_lon} {center_lat})"))
        # GeoDataFrame
        gdf = gpd.GeoDataFrame(geometry=gs)
        # Projection
        gdf.crs = "EPSG:4326"
        gdf = gdf.to_crs("EPSG:3857")
        res = gdf.buffer(
            distance=half_side,
            cap_style=3,
        )

        # Get the geom
        gdf = res.to_crs("EPSG:4326")
        geom = gdf.iloc[0]
        geojson_string = geojson.dumps(mapping(loads(geom.wkt)))
        self.geojson_dict = json.loads(geojson_string)
        return self.geojson_dict

    def clipped(self, clipped_raster: str = None) -> None:
        """Clipping the raster file"""
        # Folder to save the file
        feature_shape = shape(self.geojson_dict)
        # Clipping the raster
        with rio.open(self.raster_file) as src:
            out_image, out_transform = mask(src, [feature_shape], invert=True)
            out_meta = src.meta.copy()

        # Writing the metadata
        out_meta.update(
            {
                "driver": "GTiff",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform,
            }
        )

        # Writing the file
        with rio.open(clipped_raster, "w", **out_meta) as dest:
            dest.write(out_image)

        try:
            assert os.path.exists(clipped_raster)
        except AssertionError:
            self.log.debug("Raster data has not been clipped!")

    @staticmethod
    def with_other_raster(raster_image:str = None, other_raster:str = None, save_file:str = None):
        r"""Clip raster using other raster extent using Python GDAL
        
        Source: https://gis.stackexchange.com/questions/297460/clip-raster-using-mask-other-raster-using-python-gdal
        
        Args:\n
            raster_image: Original raster image that needs to be clipped
            other_raster: Raster image with smaller extent.
            save_file: Path to the output File, ends with tif 
        """
        maskDs = gdal.Open(other_raster, gdal.GA_ReadOnly)
        projection=maskDs.GetProjectionRef()
        geoTransform = maskDs.GetGeoTransform()
        minX = geoTransform[0]
        maxY = geoTransform[3]
        maxX = minX + geoTransform[1] * maskDs.RasterXSize
        minY = maxY + geoTransform[5] * maskDs.RasterYSize 
           
        data=gdal.Open(raster_image, gdal.GA_ReadOnly) 
        gdal.Translate(save_file,data,format='GTiff',projWin=[minX,maxY,maxX,minY],outputSRS=projection)     
        return save_file    
            