#! /usr/bin/python3

import logging
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE_DIR)

sys.path.append(BASE_DIR)
logging.basicConfig(stream=sys.stderr)

from src.flask import app as application  # noqa E402
