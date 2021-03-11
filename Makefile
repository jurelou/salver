

docker:
	docker-compose -f deploy/docker-compose.yml up -d

engine:
	 celery  -A opulence.engine.app worker --hostname=engine --logfile=/tmp/celery.log --loglevel=INFO -B
agent:
	 celery  -A opulence.agent.app  worker --hostname=agent --logfile=/tmp/celery.log

install:
	rm -rf env
	python3.8 -m venv env
	env/bin/pip install pip setuptools wheel -U
	env/bin/pip install -r requirements.txt
format:
	tox -e format
