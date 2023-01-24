# generic-backupy-api
api for generic-backupy app

## Setup the project
Clone the project
```
git clone https://github.com/generic-backupy/generic-backupy-api.git
cd generic-backupy-api
```

Copy the .env files manually or use the sh script `./setup-env.sh`
```
cp .env.example .env
cp django.env.example django.env
cp postgres.env.example postgres.env
cp redis.env.example redis.env
```

Adjust the .env files to your needs (change the passwords for production!!!)
If the port 8005 is already in use, pleas change the API_PORT in the .env file.

Run the `./setup.local.sh` file, to setup the database, and to create a root user.
```
./setup.local.sh
```

For production setup use the `setup.prod.sh` script.

After that you can run the application with
```
./docker-compose.local.sh up
```

or to run it in background you can use
```
./run.local.sh
```

## Tests
Run the tests locally with the command
```
./manage.py.local.sh test
```

## Debug with Intellij

1. open the project as django project (with new project, django and so on)
2. Preferences, Build, Docker - Add Docker
3. Project-Structure, SDK, Add Python SDK with Docker compose (add first the normal yaml, and then the dev)
4. Project-Structure, Module, add the details for django project (settings-file, manage file, etc)
5. Edit Configuration, Django, Host 0.0.0.0 (not localhost!), Port 8000, Interpreter (the interpreter which we created in 3)

### Debug Tests
If there is an error, when you debug the test, try to add the environment to your Intellij runtime
```
DJANGO_SETTINGS_MODULE=genericbackupy.settings.development;PYTHONUNBUFFERED=1
```
where the DJANGO_SETTINGS_MODULE is specified.
Also add the option `--no-input` to the option field, to prevent a stop if you restart the
session, without django deleted the test-database. With this option, it will automatically delete
the test database on start.

## Translations
### Create/Update lang file
`./manage.py.dev.sh makemessages -l de --no-location`

to update all files (doesn't work currently):
`./manage.py.dev.sh makemessages -a`

### Compile lang files
`./manage.py.dev.sh compilemessages`

## Deployment final

## Local
own docker file
## Server
### database 
own docker file
### server
own docker file

## Redis
### TODO SSL
Find a solution to use ssl, to use the redis container as external service.
Currently SSL should be deactivated, because it isn't working with a self-signed certificate.
If we use the flag ssl_cert_reqs to prevent the cert check, we get an error, that the client (we)
doesn't provide a certificate. So we also need to integrate the client cert, but there is 
no information in the documentation for django-rq.

### Add TLS files
Navigate to the redis folder, and execute the `generate-tls-files.sh` script.
```bash
cd /redis
./generate-tls-files.sh
```

### Tips

## docker container uses ip address of the local network range
This can happen, if there are two much docker networks, or if the network range is configured for the
range of the local network.

For the first case execute `docker network prune` and restart the containers (down and up)

## Production Deployment
Clone the project
```
git clone https://github.com/generic-backupy/generic-backupy-api.git
cd generic-backupy-api
```

Copy the .env files manually or use the sh script `./setup-env.sh`
```
cp .env.example .env
cp django.env.example django.env
cp postgres.env.example postgres.env
cp redis.env.example redis.env
```


After that, change the port in postgres.env to the postgres mappping port
from .env, because the db should be deployed externally, and they use
different docker networks.
Also use the ip address of the machine, where you deploy the database for the host
in postgres.env


After that, change the port in the redis.env file to the mapping port of the .env file.
Also change the host to the ip address of the machine. Also enable tls in the
redis.env file.

### Generate the SSL Keys
To protect the communication with redis and postgres, you need to provide
ssl certificates for it.

#### Postgres
You need to change the user for the server files to the user id 999 (postgres) with `chown 999 server.crt`
