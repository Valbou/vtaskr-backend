#!/usr/bin/env bash

# Third script to run to generate a compiled .mo file 

# To use it pass the folder app to trad
# ./trad_compile_mo users
# ./trad_compile_mo tasks

source ../bin/activate

if [ -n "$1" ]
then
    # Compile to MO Files
    pybabel compile -i src/$1/translations/de/LC_MESSAGES/$1.po -o src/$1/translations/de/LC_MESSAGES/$1.mo
    pybabel compile -i src/$1/translations/en/LC_MESSAGES/$1.po -o src/$1/translations/en/LC_MESSAGES/$1.mo
    pybabel compile -i src/$1/translations/es/LC_MESSAGES/$1.po -o src/$1/translations/es/LC_MESSAGES/$1.mo
    pybabel compile -i src/$1/translations/fr/LC_MESSAGES/$1.po -o src/$1/translations/fr/LC_MESSAGES/$1.mo
    pybabel compile -i src/$1/translations/it/LC_MESSAGES/$1.po -o src/$1/translations/it/LC_MESSAGES/$1.mo
    pybabel compile -i src/$1/translations/pt/LC_MESSAGES/$1.po -o src/$1/translations/pt/LC_MESSAGES/$1.mo
else 
    echo "No domain given";
fi
