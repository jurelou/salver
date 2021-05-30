

[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![python version](https://img.shields.io/badge/python-3.8-blue)](https://www.python.org/)

# Install

requires docker && python >= 3.8
```
make install # installe les dépendances python
source env/bin/activate # active l'environnement virtuel

make docker # crée les dockers (BDD / kafka)
make bootstrap  # crée les index, prépare les BDD

make agent
make engine

python toto.py # test: crée un scan

```

# TODO

connectors: neo4J/eladstic make a caching mechanism usique a Q and sched() to flush the queue every X sec

### API rest:

- lister les agents
- lister les collect pour un scan donné
- lister lesscan
- creer un scan (comme dans toto.py)

<<<<<<< HEAD
-


# PORTS

- Mongo GUI: http://locahost:8017
- Kafka GUI: http://localhost:8000/
- Kibana: http://localhost:5601
=======
- 
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
