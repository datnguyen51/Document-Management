### Install Python

```
$ sudo apt update
$ sudo apt install software-properties-common
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt install python3.7 -y
$ python3.7 -V
$ sudo apt-get install python3.7-dev python3.7-venv
$ sudo apt-get install libpq-dev
$ sudo apt-get install python3 python-dev python3-dev \
     build-essential libssl-dev libffi-dev \
     libxml2-dev libxslt1-dev zlib1g-dev \
     python-pip
```

### Install Postgres
```
$ sudo apt-get install wget ca-certificates
$ wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
$ sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
$ sudo apt-get update
$ sudo apt-get install postgresql-11
```

```
$ mkdir edu-service
$ cd edu-service

$ python3.7 -m venv .
$ source bin/activate

$ git clone https://gitlab.com/truongnd96/edu-service.git repo
$ cd repo

$ pip install -r requirements.txt

$ sudo -su postgres psql
$ create user eduowner with password 'edu@2020';
$ create database edu;
$ alter user eduowner with superuser;

$ cd alembic
$ mkdir versions
$ cd ..
$ alembic revision --autogenerate -m "init db"
$ alembic upgrade head
