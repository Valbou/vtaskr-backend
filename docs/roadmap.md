# vTaskr Backend - ROADMAP

Welcome to the vTaskr Roadmap.
Here you can find features we need to add to upgrade version number.
As vTaskr is an non profit project without fulltime dev, no release date can be fournished.

## Go to v0.1.0

The first goal is to permit a basic use of a to do list.
An heavy base is needed in term of rights/permissions.

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
- [x] Add gunicorn
- [x] Start a frontend developpement in an other git repository
- [x] User can manage groups (create, read, update, delete and achieve)
- [x] User can manage roles (create, read, update, delete and achieve)
- [x] User can manage role types (create, read, update, delete and achieve)
- [x] User can manage rights (create, read, update, delete and achieve)
- [x] User can't access to tasks not owned by at least one of his groups
- [x] User can delete his account efficiently (cannot delete a user if user has admin role on 2 groups or more !)
- [x] Add filters on list endpoints (filter groups according to role or filter rights according to a group etc...)
- [ ] When paginated result is asked, provide some helpers like page max number or the number of items available.
- [x] User can't modify tasks without the required role
- [x] User can invite another in a non private group
- [x] User can invite another user in a group with a specific role
- [ ] Telegram bot integration
- [x] Add a basic dev documentation
- [x] Cron job to send today and tomorrow tasks

## Go to v0.2.0

Start v0.2.0 dev when frontend is ok with v0.1.0

- [ ] Code events developments
- [ ] Create tasks in to do lists template
- [ ] Transform a template into a todolist
- [ ] Use triggers to auto apply a template
- [ ] Task reccurence
- [ ] Weekly/Daily email with tasks of the period
- [ ] Sub tasks
- [ ] Project task organisation
- [ ] Tasks status (blocking) that block parent task
- [ ] Tasks association, link another task (nonblocking link)
- [ ] Tasks assignation to a group member
- [ ] Reminders/Alerts - Telegram/Email
- [ ] Add .ics generator (iCalendar format)

## Go to v0.3.0

Start v0.3.0 dev when frontend is ok with v0.2.0

- [ ] Add tasks from telegram
- [ ] Add tasks from .ics sent by email
- [ ] Add tasks from github/gitlab/forgejo
- [ ] Add Keycloak integration
- [ ] Add hooks for external integration

More in the futur...
