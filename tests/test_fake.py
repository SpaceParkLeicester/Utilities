import logging
from logging import config

config.fileConfig("logger.ini")

def test_template():
  """Testing the template"""
  # Delete this file .py file
  try:
    logging.info("May The Force Be With You")
  except ImportError:
    logging.error("Something went wrong with the workflow")
