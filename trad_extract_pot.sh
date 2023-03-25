source ../bin/activate

# Generate PO Templates Files
pybabel extract -F babel.cfg -o vtasks/$1/locales/messages.pot vtasks/$1
