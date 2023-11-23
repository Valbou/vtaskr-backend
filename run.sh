source ../bin/activate

gunicorn src.flask:app --bind=0.0.0.0 --access-logfile access.log --error-logfile errors.log --log-level 'warning'
