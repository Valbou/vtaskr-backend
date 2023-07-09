source ../bin/activate

gunicorn vtaskr.flask:app
