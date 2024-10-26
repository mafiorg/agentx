FROM python:3.11.4-slim-buster as builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

# lint
# RUN pip install --upgrade pip
# RUN pip install flake8==6.0.0
COPY . .

# RUN flake8 .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt



FROM python:3.10

RUN mkdir -p /home/app

RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/server
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat sqlite3 libsqlite3-dev

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*
RUN pip install gunicorn==21.2.0

# copy project
COPY . $APP_HOME

# TODO: remove after add postgresql
RUN mkdir sqlite

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

EXPOSE 80

CMD python manage.py migrate && python manage.py runserver 80
