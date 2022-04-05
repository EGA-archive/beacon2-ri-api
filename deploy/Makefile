all: down up load reindex rebuild

load:
	mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file data/analyses*.json --collection analyses
	mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file data/biosamples*.json --collection biosamples
	mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file data/cohorts*.json --collection cohorts
	mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file data/datasets*.json --collection datasets
	mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file data/individuals*.json --collection individuals
	mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file data/runs*.json --collection runs
	mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file data/genomicVariations*.json --collection genomicVariations

up-db:
	docker-compose up -d db && \
	docker-compose up -d mongo-express

up: up-db
	docker-compose up -d beacon

rebuild:
	docker-compose rm -sf beacon && \
	docker-compose build beacon && \
	docker-compose up -d beacon && \
	docker-compose logs -f beacon

logs:
	docker-compose logs -f beacon

relaunch:
	docker-compose up beacon

down:
	docker-compose down

verify:
	beacon-verifier http://localhost:5050/api/

reindex:
	python3 reindex.py

# only works with justfile (https://github.com/casey/just#recipe-parameters)
test COLLECTION REQUEST:
	http POST http://localhost:5050/api/{{COLLECTION}}/ --json < {{REQUEST}}
