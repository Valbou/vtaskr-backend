# vTasks Backend
An open-source to do list application for personnal use.

Development in progress... Not ready for use. We aim to use the hexagonal architecture, and assume it, even if it seems overkill/overengineering for a small app.

![License LGPLv3](https://img.shields.io/badge/license-LGPLv3-blue "License LGPLv3")
![Python v3.8](https://img.shields.io/badge/python-v3.8-blue "Python v3.8")
![Tests 60 passed](https://img.shields.io/badge/tests-60%20passed-green "Tests 60 passed")
![Coverage 86%](https://img.shields.io/badge/coverage-86%25-green "Coverage 86%")
![Code quality A](https://img.shields.io/badge/code%20quality-A-green "Code quality A")

## Technical informations

All commands are given from the repository root folder (where you find .git).
You may need to run it in your python virtual environment.

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
