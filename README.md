# Text Shuffler

A small Django app to shuffle text inside uploaded files.

## Installation 

Prerequisites
- Python 3.12
- Pipenv

```powershell
pipenv install --dev
pipenv run python -m playwright install
pipenv shell
```

Set up the Django project

```powershell
python manage.py migrate
python manage.py runserver
```