all: down up clean generate load reindex rebuild

generate:
	sh generate_json.sh 10

load:
	python3 load_json.py --file data/analyses*.json --collection analyses --db "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin"
	python3 load_json.py --file data/biosample*.json --collection biosamples --db "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin"
	python3 load_json.py --file data/cohorts*.json --collection cohorts --db "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin"
	python3 load_json.py --file data/datasets*.json --collection datasets --db "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin"
	python3 load_json.py --file data/genomicVariations*.json --collection genomicVariations --db "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin"
	python3 load_json.py --file data/individuals*.json --collection individuals --db "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin"
	python3 load_json.py --file data/runs*.json --collection runs --db "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin"

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