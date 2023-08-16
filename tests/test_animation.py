from utilities.utils import Loader
from time import sleep


def test_loading():
    """Testing the loading animation"""
    with Loader("Loading with context manager..."):
        for _i in range(10):
            sleep(0.25)

    loader = Loader("Loading with object...", "That was fast!", 0.05).start()
    for _i in range(10):
        sleep(0.25)
    loader.stop()
