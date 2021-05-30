re: redocker bootstrap

redocker:
	docker-compose -f ./deploy/docker-compose-engine.yml down -v
	docker-compose -f ./deploy/docker-compose-engine.yml up --build --force-recreate -d

docker:
	docker-compose -f ./deploy/docker-compose-engine.yml up -d

# api:
# 	uvicorn salver.api.main:app --reload

engine:
<<<<<<< HEAD
	docker-compose up --force-recreate
=======
	docker-compose up
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96

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
	pre-commit run --all-files -v

bootstrap:
	./scripts/wait_services_up.sh
	python -m scripts.bootstrap_kafka
	python -m scripts.bootstrap_mongodb
	python -m scripts.bootstrap_kibana
	python -m scripts.bootstrap_elasticsearch

	# python scripts/bootstrap_mongodb.py

sloc:
	pygount --format=summary ./salver

clean:
	docker-compose -f ./deploy/docker-compose-engine.yml -f ./docker-compose.yml down -v
	docker container prune -f
	docker network prune -f
	docker volume prune -f
