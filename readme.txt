How to start server

1. Create virtual env using virtualenv or anaconda 
2. Activate enviroment
3. Install using pip:
 - pip install django
 - pip install djangorestframework
 - pip install psycopg2
 - pip install django-rest-swagger

4 Create database in postgres named pai:
 - CREATE DATABASE pai; 
5 Then:
  - python manage.py makemigrations
  - python manage.py migrate
5 Run in cmd: python manage.py runserver 
	
