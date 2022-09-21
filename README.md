# Dockerized Cinema API

API service for cinema management written on DRF

## Installing using Github
### Mac Os
```shell
git clone https://github.com/MarkoKhodan/restaurant-voting-api
cd restaurant-voting-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export DB_HOST=<your db hostname>
export DB_NAME=<your db name>
export DB_USER=<your db username>
export DB_PASSWORD=<your db user password>
export SECRET_KEY=<your secret key>
python manage.py runmigtarions
python manage.py runserver
```
### Windows
```shell
git clone https://github.com/MarkoKhodan/restaurant-voting-api
cd restaurant-voting-api
python3 -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
set DB_HOST=<your db hostname>
set DB_NAME=<your db name>
set DB_USER=<your db username>
set DB_PASSWORD=<your db user password>
set SECRET_KEY=<your secret key>
python manage.py runmigtarions
python manage.py runserver
```


### Run with docker

```shell
docker-compose build
docker-compose up
```

Getting access


```shell
python manage.py createsuperuser
```
Then, login with http://127.0.0.1:8000/api/user/token/



Features

- JWT authenticated
- Admin panel /admin/
- Documentation is located at /api/doc/swagger/
- Creating Employees and Restaurants allowed only for admin
- Creating Menus allowed only for restaurants staff
- Voting is possible for employees
- Only one vote per day