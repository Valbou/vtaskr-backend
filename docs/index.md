# vTaskr Backend Documentation (Dev Doc)

vTaskr is a to do list application for personnal use.
The project is under active developpement, but not ready for production. Some breaking changes may appear without warning.

You are visiting the **backend developer documentation**.  
Code repository available here: [vTaskr Backend](https://github.com/Valbou/vtaskr-backend).  
If you are looking for frontend go to [vTaskr Frontend](https://github.com/Valbou/vtaskr-frontend).  

vTaskr Backend use CPython 3.10+, Flask and Gunicorn. Databases needed: Postgres 15+, Redis 6+.

To See more details about dependencies, you can read pyproject.toml file.

![License LGPLv3](https://img.shields.io/badge/license-LGPLv3-blue "License LGPLv3")
![Python v3.10](https://img.shields.io/badge/python-v3.10-blue "Python v3.10")
![Tests 483 passed](https://img.shields.io/badge/tests-483%20passed-green "Tests 483 passed")
![Coverage 90%](https://img.shields.io/badge/coverage-90%25-green "Coverage 90%")
[![CodeFactor](https://www.codefactor.io/repository/github/valbou/vtaskr-backend/badge)](https://www.codefactor.io/repository/github/valbou/vtaskr-backend)
![API](https://img.shields.io/website?url=https%3A%2F%2Fapi.vtaskr.com)

## New to vTaskr

To install vTaskr on premise: [Getting Started](./getting-started.md).

## The project

vTaskr is a project to provide features to manage time and free your mind. This is possible if it's easy to use it.  
So productivity and efficiency are mandatory to keep using it. It's the primary focus !  
To continue to develop vTaskr with pleasure, we need to keep base code clear, and clearly separate concerns.  

To contribute, please, keep this elements in mind.  

### Git Strategy

Master branch is not really clean (my fault), but I aim to tend to a cleaner history. One feature, one branch with squashed commits.  
After merge, branch is deleted.  

A **release is done after**: all required features are done, documentation is up to date, translations are up to date, all unit tests passed, some manual end user tests are made, ideally at least a review is done.  

### Repository structure

At first level you can find:  
 - **alembic**: used to version database and track migrations.  
 - **docs**: used to provide this documentation with Mkdocs.  
 - **hooks**: some tools to help to be a good developer, and limit commits with bad PEP8 practicises before any CI. Need to be installed manually using shell command provided inside.  
 - **src**: vTaskr source code.  
 - **tests**: vTaskr tests (unit tests and integration tests).  
 - **LICENSE**: just to precise it's a GNU GPL v3 project.  
 - **pyproject.toml**: manage project dependencies and configs.  
 - **README.md**: to help users to find the doc :).  
 - **run.sh**: just a helper to run a dev HTTP server locally (if you need it).  
 - **template.env**: a .env template to keep up to date !  
 - **trad_*.hs**: some helpers files to manage translation.  

Actually, the project is splitted in "apps" in the "src" sub directory:  
 - **base**: provide project global utilitaries (like a backend [home page](https://api.vtaskr.com))  
 - **colors**: provide elements to manage colors (but may disapear in a near futur to limit dependecies. Initially separated to limit duplicate code...)  
 - **events**: provide a basic internal event service to pass data cross apps.  
 - **libs**: provide external lib specific adapters.  
 - **notifications**: provide features to send informations to a user.  
 - **ports**: provide all bases classes to inherit from, for your adapters.  
 - **static**: provide some assets to insert in backend features like email or backend [home page](https://api.vtaskr.com).  
 - **tasks**: provide elements to manage "to do lists", project management.  
 - **users**: provide elements to manage users authentication and authorizations. This app may be replaced by any Identity and Access Manager (IAM) like Keycloak.  

Excepting "libs", "ports", "static", all apps can be seen as a microservice, and could be separated in many dockers instances for scalability.  

### Roadmap

The roadmap is actually not totally fixed. It moves depending on early adopters feedbacks and dev constraints.  
But you can see the [main direction here](./roadmap.md).  
