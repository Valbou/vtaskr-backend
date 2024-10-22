# Get Started

## Install vTaskr

```bash
apt install postgresql lsb-release redis
apt install git python3-venv python3-pip

python3 -m venv vtaskr-project
cd vtaskr-project
git clone git@github.com:Valbou/vtaskr-backend.git
cd vtaskr-backend
```

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
```bash
python -m mkdocs build
```

# To use your own frontend

If you want to use your own frontend, you can see the [OpenAPI documentation](https://api.vtaskr.com/documentation). ([Public Postman](https://www.postman.com/valbou/workspace/vtaskr/overview))

# To use your own mobile app

Actually no webapp or market specific application is planned.  
You can develop your own using backend API.  

# Projects using vTaskr

If you create one (frontend, backend, app...), let me a message with a link to your project.  
A list of apps using vTaskr backend will be referenced below.
