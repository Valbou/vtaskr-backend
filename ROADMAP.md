# vTaskr Backend - ROADMAP

Welcome to the vTaskr Roadmap.
Here you can find features we need to add to change version number.
As vTaskr is an non profit project without fulltime dev, no release date can be fournished.

## Go to v0.1.0
- [x] User can register
- [x] User can change profile information
- [x] User can change securely email and password
- [x] User can login securely
- [x] User can manage tasks (create, read, update, delete)
- [x] User can manage tags (create, read, update, delete)
- [x] User can't access to tasks or tags not owned
- [x] User can filter tasks with some basics filters
- [x] Add an OpenApiv3 documentation
- [x] User can associate Task and Tags together
- [x] Add alembic migrations
- [x] Check code organisation
- [x] Add gunicorn/uvicorn
- [x] Start a frontend developpement in an other git repository
- [x] User can manage groups (create, read, update, delete and achieve)
- [x] User can manage roles (create, read, update, delete and achieve)
- [x] User can manage role types (create, read, update, delete and achieve)
- [x] User can manage rights (create, read, update, delete and achieve)
- [x] User can't access to tasks not owned by at least one of his groups
- [x] User can delete his account efficiently (cannot delete a user if user has admin role on 2 groups or more !)
- [x] Add filters on list endpoints (filter groups according to role or filter rights according to a group etc...)
- [x] User can't modify tasks without the required role

## Go to v0.2.0
- [ ] Code events developments
- [ ] Add a dev documentation
- [ ] Grouping tasks in ToDo lists
- [ ] Transform a todolist into a template to reuse it.
- [ ] Task reccurence
- [ ] Weekly/Daily email with tasks of the period
- [ ] Telegram bot integration
- [ ] User can invite another user in a group with a specific role
- [ ] Sub tasks
- [ ] Tasks status (blocking) that block parent task
- [ ] Tasks association, link another task (nonblocking link)
- [ ] Tasks assignation to a group member
- [ ] Reminders/Alerts - Telegram/Email
- [ ] Add .ics generator (iCalendar format)
- [ ] Add Keycloak integration
- [ ] Add hooks for external integration

More in the futur...
