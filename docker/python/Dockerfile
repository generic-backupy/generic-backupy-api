FROM python:3.9.12-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY ./app /code
WORKDIR /code
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" > /etc/apk/repositories && echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories
# You will need this if you need PostgreSQL, otherwise just skip this
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev g++ gettext chromium-chromedriver chromium openssh
#RUN apt-get update && apt-get install --assume-yes gcc python3-dev musl-dev libffi-dev
RUN ln -fs /usr/bin/python3 /usr/bin/python
RUN pip install --upgrade pip
COPY docker/python/requirements.txt .
RUN pip install -r requirements.txt
