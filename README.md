# URLSHRT - Yet Another URL Shortener

[![Build badge](https://img.shields.io/github/workflow/status/sintezcs/yaurlshrtr/Python%20application)](https://github.com/sintezcs/yaurlshrtr/actions)

## Description
Yet Another URL Shortener is a simple URL shortener service that allows you to shorten any URL you want. 
Redis is used to store the shortened URLs. Redis timeseries addon is used to keep track of the number of clicks on the shortened URL.

### The stack
- Python 3.9
- FastAPI
- Redis

Development environment:
- Pytest
- Flake8
- Black
- Docker

## Design decisions

### Why not Python 3.10.2 (the latest one)?
In my opinion it's better to use Python that is one minor version behind the latest release.
It eliminates possible compatibility problems with 3d-party packages. 

### Why FastAPI?
FastAPI is a modern framework, based on asyncio with a lot of batteries included (validators, exceptions, etc).
It's a good choice if you want to create a fast and scalable service. We can assume that our service will be used by millions of people.
So using a non-blocking framework should be a good idea. It will allow us to scale our service easily.

### Why Redis?
Redis a really fast key-value store with a simple python API, so the POC can be built really quickly.
Using a time-series DB addon also simlifies the implementation of the link clicks analytics.

#### Downsides of Redis, and why can we scale this up for millions of records?
There are two main problems in using this approach for a real-life app:
1. Redis persists the data on disk. But it does not guarantee 100% reliability. We can configure  
it to use a combined persistence approach ([AOF + RDB](https://redis.io/docs/manual/persistence/)) 
to achieve the maximum reliability. And also use a clustered setup with replicas.
2. Memory size. If we would like to store 100 million records, we would need about 0.5TB or RAM. 
It will be a really expensive setup. To avoid this, we can use a database storage. For example, 
we can use Redis as a caching layer. While the main data will be persisted in a database (e.g. PostgreSQL or MySQL) 

### Application structure

The application is structured as follows:
```
/src/tests - unit tests for the application
/src/urlshrtr/app.py - the main application file. It also contains a healthcheck endpoint.
/src/urlshrtr/config.py - the application configuration. It uses Pydantic Settings to manage the config values.
/src/urlshrtr/error.py - helper functions for error handling.
/src/urlshrtr/handlers.py - API handlers for all url shortening methods.
/src/urlshrtr/logic.py - the business logic layer. 
/src/urlshrtr/model.py - the application data model layer.
/src/urlshrtr/redis_connector.py - the Redis connector.
/src/urlshrtr/schema.py - DTOs and request/response schemas.
/src/gunicorn_config.py - Gunicorn configuration.
```

## Running the project locally

### Requirements

You need to have Docker installed and running.
 

### Running the app
```bash
$ docker compose up
```

Then you can view [the API docs](http://localhost/docs) and make some requests.


### Running the tests

The project is using flake8 and black for linting and code formatting.
This command will run the flake8 linter and the unit tests in a container.

```bash
$ docker-compose run test
```

