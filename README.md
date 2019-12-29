## First steps

1. Create virtual env using virtualenv or anaconda
2. Activate enviroment
3. Install using pip: `pip install -r requirements.txt`
4. Create database in postgres named pai: `CREATE DATABASE pai;`
5. Then:
    ```
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Create superuser to use admin panel (`/admin`): `python manage.py createsuperuser`
7. Run server: `python manage.py runserver` 
	
