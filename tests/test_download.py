from utilities.download import download_url
import logging
from logging import config

config.fileConfig("logger.ini")


def test_link(uol_logo):
    """Testing download status"""
    link = download_url(log=logging)
    status = link.is_downloadable(url_link=uol_logo)
    assert status == True
