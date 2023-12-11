"""
    Get the Latitude and Longitude for a given Tile Coordinates
"""
from math import atan, degrees, pi, sinh


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


if __name__ == "__main__":
    top_left = (130887, 84606)
    down_right = (130888, 84607)

    tile = GoogleTileZoom()
    left, upper, _, _ = tile.tile_edges(x=top_left[0], y=top_left[1], z=18)
    _, _, right, lower = tile.tile_edges(x=down_right[0], y=down_right[1], z=18)
    print([[lower, left], [upper, right]])
