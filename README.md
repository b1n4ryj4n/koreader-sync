# koreader-sync

## Description

Quick and dirty implementation of the KOReader (https://github.com/koreader/koreader) sync service.
I found stock implementation (https://github.com/koreader/koreader-sync-server) too heavy for my personal needs. This is a fork of https://github.com/myelsukov/koreader-sync but i rewrite the complete code.
 
## Dependencies

* FastAPI : https://github.com/tiangolo/fastapi
* TinyDB: https://github.com/msiemens/tinydb
* Uvicorn: https://www.uvicorn.org/

## Install and run

```bash
> pip install -r requirements.txt

> uvicorn kosync:app --host 0.0.0.0 --port 8081

```

## Or via Docker

```bash
> docker build --rm=true --tag=kosync .

> docker-compose up -d

```

## Connection

* Use http://IP:8081 as custom sync server
* Recommendation: Setup a reverse proxy for example with Nginx Proxy Manager (https://nginxproxymanager.com/) to connect with https

## Changelog

## [0.0.1] - 2021-05-15
### Added
- First version