.PHONY: clean

redocker:
	docker-compose -f ./deploy/docker-compose.yml down -v
	docker-compose -f ./deploy/docker-compose.yml up --build --force-recreate -d

docker:
	docker-compose -f ./deploy/docker-compose.yml up -d

test:
	ENV_FOR_DYNACONF=local python test.py
localengine:
	ENV_FOR_DYNACONF=local celery  -A salver.engine.celery_app worker -B

localagent:
	ENV_FOR_DYNACONF=local celery  -A salver.agent.celery_app worker --hostname agent@`openssl rand -hex 4`

install:
	rm -rf env
	python3.8 -m venv env
	env/bin/pip install pip setuptools wheel -U
	env/bin/pip install .[dev]

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

# test:
# 	pytest -s ./tests/

lint:
	tox -elint

sloc:
	pygount --format=summary ./salver
