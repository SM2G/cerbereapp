# Cerbere App

![alt text](https://raw.githubusercontent.com/SM2G/cerbereapp/master/cerbereapp/static/cerbereapp/logo_v2.png "CerbereApp")

## Description

Web-based document lifecycle managment solution. Open source version with basic functionnalities.

## Features
+ Mysql database support
+ Django ORM
+ Salted SHA1 password storage

## Configuration

```bash
virtualenv venv -p python3.5
source venv/bin/activate
sudo apt-get install libmysqlclient-dev
pip install --upgrade pip
pip install -r requirements.txt
cp cerbereapp/settings.py.sample cerbereapp/settings.py
# Adapt... and conquer.
```

## Features Roadmap
+ ~~Login/logout~~
+ ~~Encrypted password storage~~
+ ~~Account managment~~
+ ~~Add/remove/manage document models~~
+ ~~Add/remove/manage profiles~~
+ ~~Add/remove/manage employees~~
+ ~~Add/remove/manage actual documents~~
+ ~~Upload document scans~~
+ Pretty Dashboard
+ Add compressor for static files
+ E-mail reporting
+ Create guest accounts
