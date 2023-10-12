# Docker Flask MongoDB App

## run

    docker-compose up && flask --app app.py --debug run

## Init

please change the path in .env

then run `docker compose up`

to remove the .env file from staging (commiting)
 
    echo "REL_PATH=$(pwd)" > .env
    git rm .env --cached
    git commit -m "Stopped tracking .env File"

### Todo

- add mongodb client to the app
- add a routes to view database from app
- 
