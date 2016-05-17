# Cerbere App

## Description

Web-based document lifecycle managment solution.

## Features
+ Mysql database support
+ Django ORM
+ Salted SHA1 password storage

## Configuration

```bash
virtualenv venv -p python3.5
source venv/bin/activate
sudo apt-get install libmysqlclient-dev
pip install -f requirements.txt
```

## Features Roadmap
+ ~~Login/logout~~
+ ~~Encrypted password storage~~
+ Account managment
+ Add/remove/manage document models
+ Add/remove/manage profiles
+ Add/remove/manage employees
+ Add/remove/manage actual documents
+ Design a pretty Dashboard
+ E-mail sending
+ Upload document scans
+ Create guest accounts
+ Advanced guest accounts
