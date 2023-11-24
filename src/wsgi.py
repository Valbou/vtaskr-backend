#! /usr/bin/python3

import logging
import os
import sys

from .flask import app as application

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE_DIR)

sys.path.append(BASE_DIR)

logging.basicConfig(stream=sys.stderr)

application.secret_key = os.getenv(
    "SECRET_KEY", "YM/92:>Dhqv=7p8+ixY=By?4i(%TU5L;W+4=dboG="
)
