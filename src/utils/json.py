"""Function to read nested JSON file"""
import json
from typing import Dict


class json_file:
    """Functions related to JSON dictionary file"""

    def __init__(self, log: isinstance = None, file_path: str = None) -> None:
        r"""Defining variables

        Args:\n
            log: Logger ini file.
            file_path: Path to the JSON file.
        """
        self.log = log
        self.file_path = file_path

        with open(self.file_path) as f:
            self.data = json.load(f)

    @staticmethod
    def recursive_items(dictionary: Dict = None):
        """Function to iterate through nested dictionary"""
        for key, value in dictionary.items():
            if type(value) is dict:
                yield from json_file.recursive_items(value)
            else:
                yield (key, value)

    def key(self, name: str = None) -> None:
        r"""Read a key in the JSON dict file

        Args:\n
            name: Any key in JSON file.
        """
        for key, value in self.recursive_items(self.data):
            if key == name:
                return value
            else:
                self.log.debug(f"{name} is not in the URL file")
