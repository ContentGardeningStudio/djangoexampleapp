# djangoexampleapp
Example Django app to learn some of the best practices

## Getting Started
You need a Python 3.10 (or higher) virtual environment

Clone this repository & install base dependencies:
```
git clone https://github.com/ContentGardeningStudio/djangoexampleapp.git
```

## Local development
Ensure that your virtual environment is activated
1. Install dependencies
```
pip install -r requirements.txt
```
2. Create database
```
python manage.py migrate
```
3. Create admin
```
python manage.py createsuperuser
```
4. Run the application
```
python manage.py runserver
```

## Tests
Tests are in the users directory

Run the tests using `pytest`:
```
pytest
```
