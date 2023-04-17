# Django-Social-API
A simple Social Web App API using Django and Django Rest Framework

## .env file
```
SECRET_KEY = "your django secret key"
TOKEN_SECRET_KEY = "your token secret key"
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
```

## Instructions
1. Install Python, Pip and Pipenv to your machine
2. Clone or Fork this repo
3. Inside the cloned directory run ```pipenv install```
4. Run the virtual environment ```pipenv shell```
5. Run the migration command ```python manage.py migrate```
6. Create superuser ```python manage.py createsuperuser```
6. Run the development server ```python manage.py runserver```