# generic-backupy-api
api for generic-backupy app

## Debug with Intellij

1. open the project as django project (with new project, django and so on)
2. Preferences, Build, Docker - Add Docker
3. Project-Structure, SDK, Add Python SDK with Docker compose (add first the normal yaml, and then the dev)
4. Project-Structure, Module, add the details for django project (settings-file, manage file, etc)
5. Edit Configuration, Django, Host 0.0.0.0 (not localhost!), Port 8000, Interpreter (the interpreter which we created in 3)


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
