# Koreader position sync server

## Description

This is a simple implementation of the KOReader (https://github.com/koreader/koreader) position sync server for self-hosting at home which has docker support for arm and amd64 :) _This is a fork of https://github.com/myelsukov/koreader-sync but with a complete code rewrite._
 
## Dependencies

* FastAPI : https://github.com/tiangolo/fastapi
* TinyDB: https://github.com/msiemens/tinydb
* Uvicorn: https://www.uvicorn.org/
* Python-dotenv: https://saurabh-kumar.com/python-dotenv/

## Install and run

```bash
> pip install -r requirements.txt

> uvicorn kosync:app --host 0.0.0.0 --port 8081

```

## Or via Docker

```bash
> docker build --rm=true --tag=kosync:latest .

> docker-compose up -d

```

## Environment Variables

* RECEIVE_RANDOM_DEVICE_ID ("True"|"False")

Set it true to retrieve always a random device id to force a progress sync. 
This is usefull if you only sync your progress from only one device and 
usually delete the *.sdr files with some cleaning tools.


## Dockerhub

There is also a dockerhub image available if you are not able to build yourself the image.

For linux/amd64 you can use `docker pull b1n4ryj4n/koreader-sync` and for linux/arm `docker pull b1n4ryj4n/koreader-sync:arm`

## Connection

* Use http://IP:8081 as custom sync server
* Recommendation: Setup a reverse proxy for example with Nginx Proxy Manager (https://nginxproxymanager.com/) to connect with https

## Changelog

## [0.0.3] - 2021-03-20
### Added
- Added an environment variable option to receive always a random device id

## [0.0.2] - 2021-02-21
### Added
- Merged ["Dockerfile: use multi-stage build to optimize image size"](https://github.com/b1n4ryj4n/koreader-sync/pull/3)

## [0.0.1] - 2021-05-15
### Added
- First version
