"""
    Create a session to download Satellite 2D MapTile
    Doc: https://developers.google.com/maps/documentation/tile/satellite
"""
import requests
import math
from typing import Tuple
import numpy as np

class GoogleMapSession:
    """Download Google 2D Satellite map tiles"""
    
    TILE_SIZE = 256
    
    def __init__(
            self,
            log: isinstance = None,
            api_key: str = None,
            latLng: Tuple = None,
            zoom: np.int16 = None ) -> None:
        """Defining variables"""
        self.log = log
        self.api_key = api_key
        self.LatLng = latLng
        self.zoom = zoom

    @staticmethod
    def fromLatLngToPoint(latLng):
        mercator = -math.log(math.tan((0.25 + latLng[0] / 360) * math.pi))
        return {
            'x': GoogleMapSession.TILE_SIZE * (latLng[1] / 360 + 0.5),
            'y': GoogleMapSession.TILE_SIZE / 2 * (1 + mercator / math.pi)
        }

    @staticmethod
    def fromLatLngToTileCoord(latLng, zoom):
        point = GoogleMapSession.fromLatLngToPoint(latLng)
        scale = 2 ** zoom

        return {
            'x': int(point['x'] * scale / GoogleMapSession.TILE_SIZE),
            'y': int(point['y'] * scale / GoogleMapSession.TILE_SIZE),
            'z': zoom
        }    
    
    def session_id(self)-> None:
        """Create and extract session ID from a JSON response"""
        try:
            assert self.api_key is not None
        except AssertionError:
            self.log.debug("Provide an API Key")
        else:
            url = "https://tile.googleapis.com/v1/createSession?key=" + self.api_key
            data = {
                "mapType": "satellite",
                "language": "en-US",
                "region": "US"
            }
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                self.id = response_data.get("session")
                self.log.info(f"Session has been created: {id}")
                return self.id
            else:
                self.log.debug(f"Failed to create a session. Status code: {response.status_code}")
                return None
    
    def download_tile(self, file_path:str = None)-> None:
        """Download a 2D Map tile for given tile coordinates and zoom level"""
        tile_params = self.fromLatLngToTileCoord(self.LatLng, self.zoom)

        url = f"https://tile.googleapis.com/v1/2dtiles/{tile_params['z']}/{tile_params['x']}/{tile_params['y']}"
        try:
            params = {
                "session": self.id,
                "key": self.api_key
            }
        except AttributeError:
            self.log.debug("No Session ID found")
        else:
            response = requests.get(url, params=params)

            if response.status_code == 200:

                with open(file_path, "wb") as output_file:
                    output_file.write(response.content)

                self.log.info(f"Image saved to {file_path}")
            else:
                self.log.debug(f"Request failed with status code: {response.status_code}")            



if __name__ == "__main__":
    import os
    import logging
    from logging import config
    config.fileConfig("logger.ini")

    from dotenv import load_dotenv
    load_dotenv()

    folder = "data/test"
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, "test.png")

    latLng = (52.64295034488556, -1.164994333736257)
    zoom = 18

    maps_2d = GoogleMapSession(
        log = logging, 
        api_key = os.environ.get("GOOGLE_MAPS_API"),
        latLng = latLng,
        zoom = zoom)
    maps_2d.session_id()
    maps_2d.download_tile(file_path)


