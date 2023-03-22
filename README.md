# vTasks Backend
An open-source to do list application for personnal use.

Development in progress... Not ready for use. We aim to use the hexagonal architecture, and assume it, even if it seems overkill/overengineering for a small app.

![License LGPLv3](https://img.shields.io/badge/license-LGPLv3-blue "License LGPLv3")
![Python v3.8](https://img.shields.io/badge/python-v3.8-blue "Python v3.8")
![Tests 180 passed](https://img.shields.io/badge/tests-180%20passed-green "Tests 180 passed")
![Coverage 93%](https://img.shields.io/badge/coverage-93%25-green "Coverage 93%")
![Code quality A](https://img.shields.io/badge/code%20quality-A-green "Code quality A")

### Translations
vTasks is available in some languages (europeans): EN, ES, DE, FR, IT, PT.
Translations were made automatically by https://www.deepl.com and https://poedit.net/, and may not be accurate. Feel free to amend them if necessary !

## Technical informations

### Install project

```bash
apt install git python3-venv

python3 -m venv vtasks-project
cd vtasks-project
git clone git@github.com:Valbou/vtasks-backend.git
cd vtasks-backend
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Install translations

```bash
chmod +x trad_*
./trad_compile_mo.sh users
```

### To run flask
```bash
flask --app vtasks run
```

## Technical informations for developpers

Follow previous steps, an continue with steps below.

### Install dev dependencies

```bash
pip install -r requirements-dev.txt
```

### To run tests
```bash
python -m coverage run -m unittest -vv
```

### To see coverage
```bash
python -m coverage report
```

## How to help ?

- First you can encourage development with starring project <3
- Give us feedback in issues: what you need, what doesn't work for you...
- If you are a dev, you can submit pull request linked to issues
- If you are a polyglot, you can translate using .po files
- If you are an user, you can write an end user documentation

All with kindness, we are just humans ;)
