#!/usr/bin/env bash

# Second script to run to generate a local .po file 

# To use it pass the folder app to trad
# ./trad_locales_po notifications

source ../bin/activate

if [ -n "$1" ]
then
    # Genereate PO Files
    pybabel init -i src/$1/translations/$1.pot -l de -o src/$1/translations/de/LC_MESSAGES/$1.po
    pybabel init -i src/$1/translations/$1.pot -l en -o src/$1/translations/en/LC_MESSAGES/$1.po
    pybabel init -i src/$1/translations/$1.pot -l es -o src/$1/translations/es/LC_MESSAGES/$1.po
    pybabel init -i src/$1/translations/$1.pot -l fr -o src/$1/translations/fr/LC_MESSAGES/$1.po
    pybabel init -i src/$1/translations/$1.pot -l it -o src/$1/translations/it/LC_MESSAGES/$1.po
    pybabel init -i src/$1/translations/$1.pot -l pt -o src/$1/translations/pt/LC_MESSAGES/$1.po
else 
    echo "No domain given";
fi
