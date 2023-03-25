source ../bin/activate

# Genereate PO Files
pybabel init -i vtasks/$1/locales/messages.pot -l de -o vtasks/$1/locales/de/LC_MESSAGES/messages.po
pybabel init -i vtasks/$1/locales/messages.pot -l en -o vtasks/$1/locales/en/LC_MESSAGES/messages.po
pybabel init -i vtasks/$1/locales/messages.pot -l es -o vtasks/$1/locales/es/LC_MESSAGES/messages.po
pybabel init -i vtasks/$1/locales/messages.pot -l fr -o vtasks/$1/locales/fr/LC_MESSAGES/messages.po
pybabel init -i vtasks/$1/locales/messages.pot -l it -o vtasks/$1/locales/it/LC_MESSAGES/messages.po
pybabel init -i vtasks/$1/locales/messages.pot -l pt -o vtasks/$1/locales/pt/LC_MESSAGES/messages.po
