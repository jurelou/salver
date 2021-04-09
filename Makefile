

docker:
	docker-compose up -d

controller:
	 ENV_FOR_DYNACONF=dev celery  -A salver.controller.app worker --hostname=engine --logfile=/tmp/celery.log --loglevel=DEBUG -B

agent:
	 ENV_FOR_DYNACONF=dev celery  -A salver.agent.app  worker --hostname=agent --logfile=/tmp/celery.log

install:
	rm -rf env
	python3.8 -m venv env
	env/bin/pip install pip setuptools wheel -U
	env/bin/pip install -e ".[dev]"

format:
	tox -e black
	tox -e isort


bootstrap:
	python scripts/bootstrap_elasticsearch.py -r
	python scripts/bootstrap_elasticsearch.py
	python scripts/bootstrap_kibana.py -r
	python scripts/bootstrap_kibana.py

sloc:
	pygount --format=summary ./salver
