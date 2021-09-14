# koreader-sync

## Description

Quick and dirty implementation of the KOReader (https://github.com/koreader/koreader) sync service.
I found stock implementation (https://github.com/koreader/koreader-sync-server) too heavy for my personal needs.
This is a fork of https://github.com/myelsukov/koreader-sync to run koreader-flask.py in Docker.
 
## Dependencies

* Flask : http://flask.pocoo.org/
* pyOpenSSL: https://pyopenssl.org/en/stable/api.html

## Install and run

```bash
> pip install flask-restful

> pip install pyopenssl

> python3 koreader-flask.py --help

```

## Or via Docker

```bash
> docker build --rm=true --tag=kosync .

> docker-compose up -d

```

## Connection

* Use http://IP:8081 as custom sync server
* Recommendation: Setup a reverse proxy for example with Nginx Proxy Manager (https://nginxproxymanager.com/) to connect with https

## Modify according to your needs

Do whatever you want to
