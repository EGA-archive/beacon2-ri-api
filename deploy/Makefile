all: down up clean load reindex rebuild

load:
	mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file data/biosample*.json --collection biosamples
	mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file data/cohorts*.json --collection cohorts
	mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file data/datasets*.json --collection datasets
	mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file data/individuals*.json --collection individuals
	mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file data/runs*.json --collection runs
	mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file data/genomicVariations*.json --collection genomicVariations

clean:
	rm -rf data beacon-v2-Models beacon-framework-v2

up-db:
	docker-compose up -d db && \
	docker-compose up -d mongo-express

up:
	docker-compose up -d db && \
	docker-compose up -d mongo-express && \
	docker-compose up -d beacon

rebuild:
	docker-compose rm -sf beacon && \
	docker-compose build beacon && \
	docker-compose up -d beacon && \
	docker-compose logs -f beacon

down:
	docker-compose down

verify:
	beacon-verifier http://localhost:5050/api/

reindex:
	python3 reindex.py