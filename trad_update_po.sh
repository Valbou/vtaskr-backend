#!/usr/bin/env bash

# Fourth script to run to generate an updated local .po file 

# To use it pass the folder app to trad
# ./trad_update_po users
# ./trad_update_po tasks

source ../bin/activate

if [ -n "$1" ]
then
    # Genereate PO Files
    pybabel update -i src/$1/translations/$1.pot -l de -o src/$1/translations/de/LC_MESSAGES/$1.po
    pybabel update -i src/$1/translations/$1.pot -l en -o src/$1/translations/en/LC_MESSAGES/$1.po
    pybabel update -i src/$1/translations/$1.pot -l es -o src/$1/translations/es/LC_MESSAGES/$1.po
    pybabel update -i src/$1/translations/$1.pot -l fr -o src/$1/translations/fr/LC_MESSAGES/$1.po
    pybabel update -i src/$1/translations/$1.pot -l it -o src/$1/translations/it/LC_MESSAGES/$1.po
    pybabel update -i src/$1/translations/$1.pot -l pt -o src/$1/translations/pt/LC_MESSAGES/$1.po
else 
    echo "No domain given";
fi
