
# The project vTaskr

vTaskr is a project to provide features to manage time and free your mind. This is possible if it's easy to use it.  
So productivity and efficiency are mandatory to keep using it. It's the primary focus !  
To continue to develop vTaskr with pleasure, we need to keep base code clear, and clearly separate concerns.  

To contribute, please, keep this elements in mind.  

[TOC]

## Git Strategy

Master branch is not really clean (my fault), but I aim to tend to a cleaner history. One feature, one branch with squashed commits.  
After merge, branch is deleted.  

We are using a ["conventional commit"](https://www.conventionalcommits.org/en/v1.0.0/) like, to help to keep clear commits.  

A **release is done after**: all required features are done, documentation is up to date, translations are up to date, all unit tests passed, some manual end user tests are made, ideally at least a review is done.  

## Repository structure

At first level you can find:  

- **alembic**: used to version database and track migrations.  
- **docs**: used to provide this documentation with Mkdocs.  
- **hooks**: some tools to help to be a good developer, and limit commits with bad PEP8 practicises before any CI. Need to be installed manually using shell command provided inside.  
- **src**: vTaskr source code.  
- **tests**: vTaskr tests (unit tests and integration tests).  
- **LICENSE**: just to precise it's a GNU GPL v3 project.  
- **pyproject.toml**: manage project dependencies and configs.  
- **README.md**: to help users to find the doc 😇.  
- **run.sh**: just a helper to run a dev HTTP server locally (if you need it).  
- **template.env**: a .env template to keep up to date !  
- **trad_*.hs**: some helpers files to manage translation.  

Actually, the project is splitted in "apps" in the "src" sub directory:

- **base**: provide project global utilitaries (like a backend [home page](https://api.vtaskr.com)).
- **colors**: provide elements to manage colors (but may disapear in a near futur to limit dependecies. Initially separated to limit duplicate code...).  
- **events**: provide a basic internal event service to pass data cross apps.  
- **libs**: provide external lib specific adapters.  
- **notifications**: provide features to send informations to a user.  
- **ports**: provide all bases classes to inherit from, for your adapters.  
- **static**: provide some assets to insert in backend features like email or backend [home page](https://api.vtaskr.com).  
- **tasks**: provide elements to manage "to do lists", project management.  
- **users**: provide elements to manage users authentication and authorizations. This app may be replaced by any Identity and Access Manager (IAM) like Keycloak.  

Excepting "libs", "ports", "static", all apps can be seen as a microservice, and could be separated in many dockers instances for scalability.  

## Apps structure

To help developers to find the right file in the good folder, we use an app structure like follow:

- **events**: this folder store observers and app events registry (to send and receive events from/to an other app).
- **hmi**: store files relative to Human Machine Interfaces, like HTML pages, API, CLI etc... and helpers like DTO etc... This views files may use dedicaded libs like Flask or FastAPI etc... and need a specific folder for each dependendy.
- **managers**: store files to manage models (use dependency injection to transparently store and retrieve data).
- **models**: core models for the app. No external lib dependency here (only python batteries included code).
- **persistence**: contain ports and adapters to access data storage (ORM, SQL/NoSQL, file system etc...). With a sub folder for each lib used (SQLAlchemy, Pewee, Pony...).
- **services**: store all services usable by a view.
- **translations**: to store... translations (.pot, .po and .mo files).
- **flask_config.py**: to setup some dedicaded config to flask. Feel free to create another file for another view lib respecting this pattern: mylib_config.py.
- **settings.py**: specific settings for the app, need at least a APP_NAME value.

This code structure permit to move easily to a new lib with a limited rewrite scoped in the lib folder. We can imagine concurrent use of some libs in the same repo. Why not a Flask implementation and a FastAPI side by side, then you just need to run.sh --flask or run.sh --fastapi to swith !

**Feel free to discuss about this code organisation if you have found a better way to do it !**

## Deep dive into apps:

- [Users](./users/index.md)
- [Tasks](./tasks/index.md)
- [Notifications](./notifications/index.md)
- [Events](./events/index.md)
