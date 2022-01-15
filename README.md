# Koreader position sync server

## Description

This is a simple implementation of the KOReader (https://github.com/koreader/koreader) position sync server for self-hosting at home which has docker support for arm and amd64 :) _This is a fork of https://github.com/myelsukov/koreader-sync but with a complete code rewrite._
 
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

## Dockerhub

There is also a dockerhub image available if you are not able to build yourself the image.

For linux/amd64 you can use `docker pull b1n4ryj4n/koreader-sync` and for linux/arm `docker pull b1n4ryj4n/koreader-sync:arm`

## Connection

* Use http://IP:8081 as custom sync server
* Recommendation: Setup a reverse proxy for example with Nginx Proxy Manager (https://nginxproxymanager.com/) to connect with https

## Changelog

## [0.0.1] - 2021-05-15
### Added
- First version
