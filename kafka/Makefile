kafka:
	docker-compose -f docker-compose.yml up -d

engine:
	docker run --rm --network kafka_opulence  -v `pwd`:/opulence toto faust -A engine worker

agent:
	docker run --rm --network kafka_opulence  -v `pwd`:/opulence toto faust -A agent worker