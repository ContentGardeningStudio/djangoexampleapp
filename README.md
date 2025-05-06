# djangoexampleapp

An example Django app to learn some of the best practices.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/ContentGardeningStudio/djangoexampleapp/blob/main/LICENSE)

## Getting started

You need a Python 3.10 (or higher) virtual environment.

Clone the repository & install the dependencies:
```
git clone https://github.com/ContentGardeningStudio/djangoexampleapp.git
```

Ensure that your virtual environment is activated, and install the dependencies:

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
