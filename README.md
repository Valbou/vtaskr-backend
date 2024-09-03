# vTaskr Backend
An open-source to do list application for personnal use.
[API vTaskr](https://api.vtaskr.com "vTaskr API") - [OpenAPI](https://api.vtaskr.com/documentation) - [Public Postman](https://www.postman.com/valbou/workspace/vtaskr/overview)

Development in progress... We aim to use the hexagonal architecture, and assume it, even if it seems overkill/overengineering for a small app.
You can follow the [Roadmap](https://github.com/Valbou/vtaskr-backend/blob/master/ROADMAP.md).

[vTaskr Frontend](https://github.com/Valbou/vtaskr-frontend)

![License LGPLv3](https://img.shields.io/badge/license-LGPLv3-blue "License LGPLv3")
![Python v3.10](https://img.shields.io/badge/python-v3.10-blue "Python v3.10")
![Tests 467 passed](https://img.shields.io/badge/tests-467%20passed-green "Tests 467 passed")
![Coverage 90%](https://img.shields.io/badge/coverage-90%25-green "Coverage 90%")
[![CodeFactor](https://www.codefactor.io/repository/github/valbou/vtaskr-backend/badge)](https://www.codefactor.io/repository/github/valbou/vtaskr-backend)
![API](https://img.shields.io/website?url=https%3A%2F%2Fapi.vtaskr.com)


### Translations
vTaskr is available in some languages (europeans): EN, ES, DE, FR, IT, PT.
Translations were made automatically by [Deepl](https://www.deepl.com) and [PoEdit](https://poedit.net/), and may not be accurate. Feel free to amend them if necessary !

## Technical informations

### Install project

```bash
apt install postgresql lsb-release redis
apt install git python3-venv python3-pip

python3 -m venv vtaskr-project
cd vtaskr-project
git clone git@github.com:Valbou/vtaskr-backend.git
cd vtaskr-backend
```

Config your own .env file (based on template.env file in project folder)
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

## Technical informations for developpers

Follow previous steps, an continue with steps below.

### Install dev dependencies

```bash
pip install .[dev]
```

### Add migrations

If you change models

```bash
alembic revision --autogenerate
```

### To run tests
```bash
python -m coverage run -m unittest -vv
```

### To see coverage
```bash
python -m coverage report
```

### To contribute

To contribute:
- clone this git repository first.
- Create a branch nammed like this: "feat-good-feature-#42".
- Use commit namming convention: "feat: my commit message".
- Run tests and check your code coverage (coverage is not just a high %)
- Make a pull request ! <3

## How to help ?

- First you can encourage development with starring project <3
- Give us feedback in issues: what you need, what doesn't work for you...
- If you are a dev, you can submit pull request linked to issues
- If you are a polyglot, you can translate using .po files
- If you are an user, you can write an end user documentation

All with kindness, we are just humans ;)
