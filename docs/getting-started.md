# Get Started

[TOC]

## Install vTaskr

No specific skill needed, but we need first to:
- Install Postgres 16 or higher
- Install Redis 6 or higher
- Install Python 3.12 or higher
- Create a python virtual environment (venv).

```bash
apt install postgresql lsb-release redis
apt install git python3-venv python3-pip

python3 -m venv vtaskr-project
cd vtaskr-project
git clone git@github.com:Valbou/vtaskr-backend.git
cd vtaskr-backend
```

You may need to create a postgres user and a database.  

Config your own .env file (based on template.env file in project folder).
Please change the default SECRET_KEY if you are using sessions.

### Install dependencies

```bash
pip install .
```
or to contribute
```
pip install -e .
```

### Install translations

```bash
chmod +x trad_*
./trad_compile_mo.sh users
```

### Run migrations

```bash
alembic upgrade head
```

### To run flask
```bash
# With Werkzeug (dev :5000)
flask --app src.flask run

# With Gunicorn (prod :8000)
gunicorn src.flask:app
```

vTaskr is now usable via CLI or API !  
If you need help, create a Github issue.


### To run Celery stack
```bash
celery --app src.celery worker -l INFO
celery --app src.celery beat -l INFO
```

### Install dev dependencies
```bash
pip install .[dev]
```

### To run tests
```bash
python -m coverage run -m unittest -vv
```

### To see coverage
```bash
python -m coverage report
```

### To build the documentation

To build a local documentation
```bash
python -m mkdocs build
```

To build and deploy github page documentation
```bash
python -m mkdocs gh-deploy --theme mkdocs
```

You can also use helpers respectively:
```bash
./build_doc.sh
./build_doc.sh deploy
```

# Project global informations

The global project organisation is available in [repository and apps structure](./global/index.md#repository-structure)
The project respect some [basic rules](./global/index.md), please read them before submitting a merge request.

# To use your own frontend

If you want to use your own frontend, you can see the [OpenAPI documentation](https://api.vtaskr.com/documentation). ([Public Postman](https://www.postman.com/valbou/workspace/vtaskr/overview))

# To use your own mobile app

Actually no webapp or market specific application is planned.  
You can develop your own using backend API.  

# Projects using vTaskr

If you create one (frontend, backend, app...), let me a message with a link to your project.  
A list of apps using vTaskr backend will be referenced below.
