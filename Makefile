# re: redocker bootstrap

redocker:
	docker-compose -f ./deploy/docker-compose-kafka.yml down -v
	docker-compose -f ./deploy/docker-compose-kafka.yml up --build --force-recreate -d

docker:
	docker-compose -f ./deploy/docker-compose-kafka.yml up -d

# api:
# 	uvicorn salver.api.main:app --reload

engine:
	ENV_FOR_DYNACONF=development python -m salver.engine.app

connectors:
	ENV_FOR_DYNACONF=development python -m salver.engine.connectors_app

agent:
	ENV_FOR_DYNACONF=development python -m salver.agent.app

install:
	rm -rf env
	python3.8 -m venv env
	env/bin/pip install pip setuptools wheel -U
	env/bin/pip install -e ".[dev]"

format:
	tox -e black
	tox -e isort
	pre-commit run --all-files

bootstrap:
	./scripts/wait_services_up.sh
	python -m scripts.bootstrap_kafka
	# python scripts/bootstrap_mongodb.py


sloc:
	pygount --format=summary ./salver
