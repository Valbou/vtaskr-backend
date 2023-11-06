source ../bin/activate

gunicorn src.flask:app --bind=0.0.0.0
