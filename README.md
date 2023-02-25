# vTasks Backend
An open-source to do list application for personnal use.

Development in progress... Not ready for use. We aim to use the hexagonal architecture, and assume it, even if it seems overkill/overengineering for a small app.

![License LGPLv3](https://img.shields.io/badge/license-LGPLv3-blue "License LGPLv3")
![Python v3.8](https://img.shields.io/badge/python-v3.8-blue "Python v3.8")
![Tests 161 passed](https://img.shields.io/badge/tests-161%20passed-green "Tests 161 passed")
![Coverage 91%](https://img.shields.io/badge/coverage-91%25-green "Coverage 91%")
![Code quality A](https://img.shields.io/badge/code%20quality-A-green "Code quality A")

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

Actually, dev dependencies are in the same requirements.

```bash
pip install -r requirements.txt
```

### To run flask
```bash
flask --app vtasks run
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
