Read the full docs here: https://opulence.readthedocs.io/en/latest/index.html

# Collectors
Collectors are responsible for collecting data accross many different OSINT sources

List of implemented collectors:

|Name | description  |
|---|---|
|badips   | check if ip is blacklisted. (ex: 91.133.35.36)  |
|Censys   |Gather information about a domain using censys   |
|ctfr   | Subdomains enumaration using certificate transparency.  |
|GoBuster dir |Directory brute force using gobuster. |
|GoBuster DNS |DNS subdomains brute force using gobuster. |
|GoBuster Vhost |Virtual host brute force using gobuster. |
|Hacker target |Uses the HackerTarget.com API to find host names. |
|Infoga |Find emails from subdomains from public sources. seach engines, PGP key servers, shodan ... |
|Nmap nse |Nmap vulnerability scan using vulscan (VulDB) |
|Nmap OS scan | Performs nmap OS detection|
|Nmap stealth scan | Performs nmap TCP stealth scan (-sS)|
|Nmap TCP connect |Performs nmap TCP connect scan (-sT) |
|Sherlock |Find usernames across social networks |
|Shodan | Gather information aout a domain using shodan|
|Sublist3r | DNS subdomains enumeration using sublist3r.|
|TheHarvester |Gather company domain from public sources. |
| PhoneInfoga|Gather information from international phone numbers. |
|Gitrob |Find sensitive files from public repositories. |
|Truffle Hog |Find keys and secrets from public repositories." |
|twint | Gather information from a user's twitter profile.|
|Zen | Find email addresses of Github users.|
|Flight Radar | Return info about a Flight |
|Profiler | OSINT HUMINT Profile Collector|
|LittleBrother |Find online presence |
|Socialscan |Find accounts from a given username/email |
|BlackWidow | Gather URLS, dynamic parameters and email addresses from a target website.|
| Kupa3|Extract javascript files and trackers. |
|WafW00f | Detect if a website is using a WAF|
|wappalyzer |Uncovers technologies used on websites |
|waybackurls |Enumerate URLS using the Wayback machine |

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
celery worker --app opulence.app --queues=collectors,engine  --autoscale=10,3
```
