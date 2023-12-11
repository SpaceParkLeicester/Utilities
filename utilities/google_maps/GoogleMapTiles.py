"""
    Google Map Tile Downloader
    Source: https://gist.github.com/bishrant/d629efb62621971ea99d
"""

import logging
import math
import os
import shutil
from math import atan, degrees, pi, sinh

import click
import requests
from dotenv import load_dotenv
from PIL import Image

from utilities.google_maps import GoogleMapSession

load_dotenv()


# Get the Latitude and Longitude for a given Tile Coordinates
class GoogleTileZoom:
    """Functions related to Google tile zoom"""

    def __init__(self) -> None:
        pass

    @staticmethod
    def mercatorToLat(mercatorY):
        return degrees(atan(sinh(mercatorY)))

    def x_to_lon_edges(self, x, z):
        """Get lat lon edges of a tile from tile coordinates"""
        tile_count = pow(2, z)
        unit = 360 / tile_count
        lon1 = -180 + x * unit
        lon2 = lon1 + unit
        return (lon1, lon2)

    def y_to_lat_edges(self, y, z):
        """Get lat lon edges of a tile from tile coordinates"""
        tile_count = pow(2, z)
        unit = 1 / tile_count
        relative_y1 = y * unit
        relative_y2 = relative_y1 + unit
        lat1 = self.mercatorToLat(pi * (1 - 2 * relative_y1))
        lat2 = self.mercatorToLat(pi * (1 - 2 * relative_y2))
        return (lat1, lat2)

    def tile_edges(self, x, y, z):
        """Getting the tile lat lon from tile coordinates"""
        lat1, lat2 = self.y_to_lat_edges(y, z)
        lon1, lon2 = self.x_to_lon_edges(x, z)
        return [lon1, lat1, lon2, lat2]


class GoogleMapTileLayers:
    ROADMAP = "v"
    TERRAIN = "p"
    ALTERED_ROADMAP = "r"
    SATELLITE = "s"
    TERRAIN_ONLY = "t"
    HYBRID = "y"

    def __init__(self, layer: str = None) -> None:
        r"""Defining variables

        Args:\n
          layer: Name of layer
        """
        self.layer = layer

    def lyr(self) -> str:
        """Return a later"""
        if self.layer == "Road Map":
            return GoogleMapTileLayers.ALTERED_ROADMAP
        elif self.layer == "Satellite":
            return GoogleMapTileLayers.SATELLITE
        elif self.layer == "Terrain":
            return GoogleMapTileLayers.TERRAIN_ONLY
        elif self.layer == "Hybrid":
            return GoogleMapTileLayers.HYBRID
        else:
            return None


class GoogleMapTileDownload:
    """
    A class which generates high resolution google maps images given
    a longitude, latitude and zoom level
    """

    def __init__(self, lat, lng, zoom=18, layer=GoogleMapTileLayers.SATELLITE):
        """
        GoogleMapDownloader Constructor
        Args:
            lat:    The latitude of the location required
            lng:    The longitude of the location required
            zoom:   The zoom level of the location required, ranges from 0 - 23
                    defaults to 12
        """
        self._lat = lat
        self._lng = lng
        self._zoom = zoom
        self._layer = layer

    def getXY(self):
        """
        Generates an X,Y tile coordinate based on the latitude, longitude
        and zoom level
        Returns:    An X,Y tile coordinate
        """

        tile_size = 256

        # Use a left shift to get the power of 2
        # i.e. a zoom level of 2 will have 2^2 = 4 tiles
        numTiles = 1 << self._zoom

        # Find the x_point given the longitude
        point_x = (tile_size / 2 + self._lng * tile_size / 360.0) * numTiles // tile_size

        # Convert the latitude to radians and take the sine
        sin_y = math.sin(self._lat * (math.pi / 180.0))

        # Calculate the y coordinate
        point_y = (
            (
                (tile_size / 2)
                + 0.5 * math.log((1 + sin_y) / (1 - sin_y)) * -(tile_size / (2 * math.pi))
            )
            * numTiles
            // tile_size
        )

        return int(point_x), int(point_y)

    def generateImage(self, **kwargs):
        """
        Generates an image by stitching a number of google map tiles together.
        Args:
            start_x:        The top-left x-tile coordinate
            start_y:        The top-left y-tile coordinate
            tile_width:     The number of tiles wide the image should be -
                            defaults to 5
            tile_height:    The number of tiles high the image should be -
                            defaults to 5
        Returns:
            A high-resolution Goole Map image.
        """
        start_x = kwargs.get("start_x", None)
        start_y = kwargs.get("start_y", None)
        tile_width = kwargs.get("tile_width", 2)
        tile_height = kwargs.get("tile_height", 2)

        # Check that we have x and y tile coordinates
        if start_x is None or start_y is None:
            start_x, start_y = self.getXY()
        # Determine the size of the image
        self.width, self.height = 256 * tile_width, 256 * tile_height

        # Bounds of the image
        self.bounds = []

        # Create a new image of the size require
        map_img = Image.new("RGB", (self.width, self.height))
        for x in range(-tile_width // 2, tile_width // 2):
            for y in range(-tile_height // 2, tile_height // 2):
                # Bounds
                self.bounds.append((start_x + x, start_y + y))
                # Google 2D Map tile Session
                base_url = f"https://tile.googleapis.com/v1/2dtiles/{self._zoom}/{str(start_x + x)}/{str(start_y + y)}"
                session = GoogleMapSession(log=logging, api_key=os.environ.get("GOOGLE_MAPS_API"))
                session_id = session.session_id()
                session_url = f"?session={session_id}&key={os.environ.get('GOOGLE_MAPS_API')}"
                url = base_url + session_url

                current_tile = str(x) + "-" + str(y)
                response = requests.get(url, stream=True)
                with open(current_tile, "wb") as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                im = Image.open(current_tile)
                map_img.paste(im, ((x + tile_width // 2) * 256, (y + tile_height // 2) * 256))
                os.remove(current_tile)
        print("Image size (pix): ", map_img.size)
        return map_img, self.bounds

    def google_tile_bounds(self):
        """Get the tile bound coordinates"""
        top_left = self.bounds[0]
        down_right = self.bounds[-1]

        tile = GoogleTileZoom()
        left, upper, _, _ = tile.tile_edges(x=top_left[0], y=top_left[1], z=self._zoom)
        _, _, right, lower = tile.tile_edges(x=down_right[0], y=down_right[1], z=self._zoom)
        return [[lower, left], [upper, right]]


def GoogleMapTileBounds(latitude, longitude, zoom, file_name):
    # Create a new instance of GoogleMap Downloader
    gmd = GoogleMapTileDownload(latitude, longitude, zoom, GoogleMapTileLayers.SATELLITE)

    print("The tile coordinates are {}".format(gmd.getXY()))

    try:
        # Get the high resolution image
        img, bounds = gmd.generateImage()
        print(f"Tile coordinate boundaries: {bounds}")
    except IOError:
        print(
            "Could not generate the image - try adjusting the zoom level and checking your coordinates"
        )
    else:
        # Save the image to disk
        folder = "data/tiles"
        if not os.path.exists(folder):
            os.makedirs(folder)
        img.save(os.path.join(folder, f"{file_name}.png"))
        print("The map has successfully been created")

        bounds_coords = gmd.google_tile_bounds()
        print(f"Tile bound coordinates: {bounds_coords}")
        return bounds_coords


@click.command()
@click.option("--latitude", default=53.64027160050831, help="Enter Latitude")
@click.option("--longitude", default=-0.2468039067285641, help="Enter Longitude")
@click.option("--zoom", default=17, help="Enter the Zoom level")
@click.option("--file_name", default="test", help="Name in which the file is saved")
def main(latitude, longitude, zoom, file_name):
    GoogleMapTileBounds(latitude, longitude, zoom, file_name)


if __name__ == "__main__":
    main()
