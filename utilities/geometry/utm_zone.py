"""
UTM-Grid zones
Source: https://en.wikipedia.org/wiki/Universal_Transverse_Mercator_coordinate_system
"""
from typing import List

class utm_grid_zones:
    """Functions related to the UTM Grid zones"""
    def __init__(
            self,
            log: isinstance = None) -> None:
        r"""Defining variables
        
        Args:\n
            log: custom logger ini function.
        """
        self.log = log
    
    @staticmethod
    def sanity_checks(grid_number: str = None)-> bool:
        r"""Perform sanity checks
        
        Args:\n
            grid_number: Provide a grid number with latitude and longitude and cardinal direction
                example: N00E33
        """
        # TODO: Perform sanity checks with grid numbers if it meets above example format
        # Return true or false
        pass
    
    @staticmethod
    def gird_tile_bounds(grid_number: str = None)-> List:
        r"""Get the geom bounds list with a grid tile number
        
        Args:\n
            grid_number: Provide a grid number with latitude and longitude and cardinal direction
                example: N00E33        
        """
        # TODO: Convert gird tile numbers into a list of bound values (left, bottom, right, top)
        # Returns a list
        pass

        

