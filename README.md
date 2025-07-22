# Django Example App

An example Django app to learn some of the best practices.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/ContentGardeningStudio/djangoexampleapp/blob/main/LICENSE)

## Package / Demo features

- Custom `User` model and associated `Profile` model
- Registration, Login, and Profile UX
- `Quote` model, to support data created by users in the app
- Unit tests for models (using `pytest`, `pytest-cov`, and `model-bakery`)
- Ruff as code linter and formatter + Pre-commit hook
- CI configuration using Github Action
- Modular settings structure, using `django-split-settings` (credit to https://github.com/wemake-services)
- Configured Django Debug Toolbar
- Base template/style leveraging `django-style` and TailwindCSS
- Management commands
- Improved security using `django-axes` and `django-permissions-policy`
- `uv` is used for Python project management

## Getting started

You need a Python 3.10 (or higher) virtual environment.

Clone the repository & install the dependencies:

```
git clone https://github.com/ContentGardeningStudio/djangoexampleapp.git
```

Install `uv`, and use it to install the project's dependencies in your virtual environment:

```
(venv) cd djangoexampleapp
(venv) uv sync
```

Initialize the database:

```
(venv) uv run manage.py migrate
```

Create the admin account:

```
(venv) uv run manage.py createsuperuser
```

Setup the site's database with needed stuff (groups/permissions, social auth, etc):

```
(venv) uv run manage.py setup_site
```

Start the Django development server:

```
(venv) uv run manage.py runserver
```

Log in with the admin account using: http://127.0.0.1:8000/admin.

## Site content creation script

Create fake data (optional):

```
(venv) uv run manage.py populate --user --is-staff
(venv) uv run manage.py populate --author
(venv) uv run manage.py populate --quote
```

## Tests

Run the tests using `pytest`:

```
(venv) pytest
```

## TODO

- Use env vars for project's secrets
- Add optional social login, using https://github.com/pennersr/django-allauth
- Add Dockerfile