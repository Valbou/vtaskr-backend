#!/usr/bin/env bash

# First script to run to extract gettext 
# uses in python files and jinja templates

# To use it pass the folder app to trad
# ./trad_extract_pot users
# ./trad_extract_pot tasks

source ../bin/activate

# Generate PO Templates Files
pybabel extract -F babel.cfg -o vtasks/$1/locales/messages.pot vtasks/$1
