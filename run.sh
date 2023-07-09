source ../bin/activate

gunicorn vtaskr.flask:app --bind=0.0.0.0
