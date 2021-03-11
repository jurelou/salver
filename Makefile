

docker:
	docker-compose -f deploy/docker-compose.yml up -d

engine:
	 celery  -A opulence.engine.app worker --hostname=engine --logfile=/tmp/celery.log --loglevel=INFO -B
agent:
	 celery  -A opulence.agent.app  worker --hostname=agent --logfile=/tmp/celery.log

format:
	tox -e format
