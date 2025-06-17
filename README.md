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

## Getting started

You need a Python 3.10 (or higher) virtual environment.

Clone the repository & install the dependencies:

```
git clone https://github.com/ContentGardeningStudio/djangoexampleapp.git
```

```
(venv) cd djangoexampleapp
(venv) pip install -r requirements.txt
```

Initialize the database:

```
(venv) python manage.py migrate
```

Create the admin account:

```
python manage.py createsuperuser
```

Setup the site's database with needed stuff (groups/permissions, social auth, etc):

```
python manage.py setup_site
```

Create fake data (optional):

```
python manage.py populate --user --is-staff
python manage.py populate --author
python manage.py populate --quote
```

Start the Django development server:

```
python manage.py runserver
```

Log in with the admin account using: http://127.0.0.1:8000/admin.

## Tests

Run the tests using `pytest`:

```
(venv) pytest
```

## TODO

- Use env vars for project's secrets
- Add optional social login, using https://github.com/pennersr/django-allauth
- Move to `uv` for project management
- Add Dockerfile