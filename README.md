# Collectors
Collectors are responsible for collecting data accross many different OSINT sources

### Initial setup

* Get the code on your local machine.
```BASH
git clone git@gitlab.com:opulence/opulence.git ; cd opulence
```

* Install dependencies and launchers:
```BASH
source install.sh
```

### Collectors requirements
## Redis

* Install redis using docker:

```BASH
docker run -d --rm --name redis-opulence -p 6379:6379 redis
```

## MongoDB

* Install redis using docker:

```BASH
docker run -d --rm --name mongo-opulence -p 27017:27017 mongo
```

## Neo4J

* Install neo using docker:

```BASH
docker run -d --rm --name neo-opulence -p 7474:7474 -p 7687:7687 neo4j
```

### Launch a collector (usefull in development)

```BASH
test-collector <name of the collector>?
```

### Start the celery worker

```BASH
celery worker -A opulence.app --queues=collectors,engine,default -l info
```
