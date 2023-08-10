"""Functions regarding URL parsing"""
import json
import os
from typing import Dict
from urllib.parse import urlparse
from urllib.request import urlopen


def url_parse(url):
    """Function to get file name and extension from a URL

    Source: https://www.slingacademy.com/article/python-get-file-name-and-extension-from-url/ # noqa: E501
    """
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = os.path.basename(path)
    filename_without_extension, file_extension = os.path.splitext(filename)
    return file_extension


def read_json_url(url) -> Dict:
    """Function to read a JSON URL

    Source: https://www.geeksforgeeks.org/how-to-read-a-json-response-from-a-link-in-python/
    """
    response = urlopen(url)
    data_json = json.loads(response.read())
    return data_json
