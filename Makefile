
redocker:
	docker-compose -f ./deploy/docker-compose.yml down -v
	docker-compose -f ./deploy/docker-compose.yml up --build --force-recreate -d

docker:
	docker-compose -f ./deploy/docker-compose.yml up -d

localengine:
	ENV_FOR_DYNACONF=local celery  -A salver.engine.celery_app worker

localagent:
	ENV_FOR_DYNACONF=local celery  -A salver.agent.celery_app worker --hostname agent@`openssl rand -hex 4`

install:
	rm -rf env
	python3.8 -m venv env
	env/bin/pip install pip setuptools wheel -U
	env/bin/python setup.py install

format:
	tox -e black
	tox -e isort
	pre-commit run --all-files

sloc:
	pygount --format=summary ./salver
