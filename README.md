# TeamUpp 

## Prerequisites 

* Docker: https://docs.docker.com/get-docker/
* Docker-compose: https://docs.docker.com/compose/install/

### Commands To Run When Starting The Project For First Time 
```bash
# build and start project
docker-compose build
docker-compose up -d

# migrate database and setup for use
docker exec -it [project folder name]_web_1 python ./manage.py migrate
```

## Design Documents
* [Database Design on Lucid](https://lucid.app/lucidchart/ce14c42f-f72c-4e86-9ab3-3ec04dd16e42/view?page=0_0#)


## Create your admin user account

This will allow you to create and delete any object in the system from `http://0.0.0.0:8000/admin`
you can also set passwords on the User models
  
```bash
# start the database and server in the background
docker-compose up -d

 docker exec -it [project folder's name]_web_1 python manage.py createsuperuser

```

## Troubleshooting

### Resetting The Database

```bash

# Make sure all containers are not running 
docker-compose down
#Start only the database container
docker-compose up -d db

#drop and recreate database
docker exec -it [project folder's name]_db_1 psql -U wisher -d postgres -c "DROP DATABASE productiondb1;"
docker exec -it [project folder's name]_db_1 psql -U wisher -d postgres -c "CREATE DATABASE productiondb1;"
docker exec -it [project folder name]_web_1 python ./manage.py migrate

```
### Checking Logs

Sometimes the database starts after the webserver causing the webserver to crash. This can be fixed by verifying this issue with `docker-compose logs`. If you see this problem. Add a space anywhere in the code and save it. The server will restart and everything should be good.


## Tests
### Running Unit Tests
```
# Start the database and server in the background
docker-compose up -d

docker exec -it [project folder name]_web_1 pytest --cov=. --cov-report html app/tests/

docker-compose down
```

### Run UI Tests

![](https://firebasestorage.googleapis.com/v0/b/cjoshmartin-f652e.appspot.com/o/Screenshot%202021-06-22%20at%2000-17-23%20Prefer%20Integration%20Tests%20Think%20twice.png?alt=media&token=830a1753-d24b-41be-aca4-97804cdafcfd)

```
# start the database and server in the background
docker-compose up -d

# run from root of projects
cd ui-tests/; npm i && $(npm bin)/cypress run; cd -

# spin down the service if you are down
docker-compose down
```
