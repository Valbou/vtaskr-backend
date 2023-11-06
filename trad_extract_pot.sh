#!/usr/bin/env bash

# First script to run to extract gettext 
# uses in python files and jinja templates

# To use it pass the folder app to trad
# ./trad_extract_pot users
# ./trad_extract_pot tasks

source ../bin/activate

if [ -n "$1" ]
then
    # Generate PO Templates Files
    pybabel extract -F babel.cfg -o src/$1/translations/$1.pot src/$1
else 
    echo "No domain given";
fi
