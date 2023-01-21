# TODO:
#   1. Test that the excel part works. It can open an excel etc
#   2. ...
from price_tracker.constants import ROOT_PATH
import os
from pathlib import Path


def test_io():
    assert ROOT_PATH.name == Path(os.getcwd()).parent.name
