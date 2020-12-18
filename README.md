# foodgram-project
![Running tests](https://github.com/olifirovai/foodgram/workflows/foodgram/badge.svg)
foodgram-project

## Site url:
[www.luckyrecipes.org](http://www.luckyrecipes.org/)

## Starting docker-compose:
```
docker-compose up --build
```
## First Start
**For the first launch**, for project functionality, go inside to the container:
```
docker exec web -t -i <WEB CONTAINER ID> bash
```
**Make migrations:**
```
python manage.py migrate
```
**To create a superuser:**
```
python manage.py createsuperuser
```


## Tech Stack
* [Python 3.8.5](https://www.python.org/)
* [Django 3.1.3](https://www.djangoproject.com/)
* [PostgreSQL](https://www.postgresql.org/)
* [Docker](https://www.docker.com/)
