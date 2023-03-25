#!/usr/bin/env bash

# Third script to run to generate a compiled .mo file 

# To use it pass the folder app to trad
# ./trad_compile_mo users
# ./trad_compile_mo tasks

source ../bin/activate

# Compile to MO Files
pybabel compile -i vtasks/$1/locales/de/LC_MESSAGES/messages.po -o vtasks/$1/locales/de/LC_MESSAGES/messages.mo
pybabel compile -i vtasks/$1/locales/en/LC_MESSAGES/messages.po -o vtasks/$1/locales/en/LC_MESSAGES/messages.mo
pybabel compile -i vtasks/$1/locales/es/LC_MESSAGES/messages.po -o vtasks/$1/locales/es/LC_MESSAGES/messages.mo
pybabel compile -i vtasks/$1/locales/fr/LC_MESSAGES/messages.po -o vtasks/$1/locales/fr/LC_MESSAGES/messages.mo
pybabel compile -i vtasks/$1/locales/it/LC_MESSAGES/messages.po -o vtasks/$1/locales/it/LC_MESSAGES/messages.mo
pybabel compile -i vtasks/$1/locales/pt/LC_MESSAGES/messages.po -o vtasks/$1/locales/pt/LC_MESSAGES/messages.mo
