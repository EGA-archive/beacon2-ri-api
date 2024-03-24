build:
	docker-compose up -d --build beacon
	docker exec deploy-db-1 /bin/bash -c 'mongo beacon -u root -p example --authenticationDatabase admin --eval "db.filtering_terms.deleteMany({})"'
	docker exec deploy-db-1 /bin/bash -c 'mongo beacon -u root -p example --authenticationDatabase admin --eval "db.analyses.deleteMany({})"'
	docker exec deploy-db-1 /bin/bash -c 'mongo beacon -u root -p example --authenticationDatabase admin --eval "db.biosamples.deleteMany({})"'
	docker exec deploy-db-1 /bin/bash -c 'mongo beacon -u root -p example --authenticationDatabase admin --eval "db.cohorts.deleteMany({})"'
	docker exec deploy-db-1 /bin/bash -c 'mongo beacon -u root -p example --authenticationDatabase admin --eval "db.datasets.deleteMany({})"'
	docker exec deploy-db-1 /bin/bash -c 'mongo beacon -u root -p example --authenticationDatabase admin --eval "db.genomicVariations.deleteMany({})"'
	docker exec deploy-db-1 /bin/bash -c 'mongo beacon -u root -p example --authenticationDatabase admin --eval "db.individuals.deleteMany({})"'
	docker exec deploy-db-1 /bin/bash -c 'mongo beacon -u root -p example --authenticationDatabase admin --eval "db.runs.deleteMany({})"'
	cd /data/vault/bio-scratch/arnau/beacon/beacon2-ri-tools-v2_test_anot
	docker cp analyses.json deploy-db-1:tmp/analyses.json
	docker cp biosamples.json deploy-db-1:tmp/biosamples.json
	docker cp cohorts.json deploy-db-1:tmp/cohorts.json
	docker cp datasets.json deploy-db-1:tmp/datasets.json
	docker cp genomicVariations.json deploy-db-1:tmp/genomicVariations.json
	docker cp individuals.json deploy-db-1:tmp/individuals.json
	docker cp runs.json deploy-db-1:tmp/runs.json
	docker cp filtering_terms.json deploy-db-1:tmp/filtering_terms.json
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/datasets.json --collection datasets
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/individuals.json --collection individuals
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/cohorts.json --collection cohorts
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/analyses.json --collection analyses
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/biosamples.json --collection biosamples
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/runs.json --collection runs
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/genomicVariations.json --collection genomicVariations
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/filtering_terms.json --collection filtering_terms
	cd .../data
	docker cp analyses.json deploy-db-1:tmp/analyses.json
	docker cp biosamples.json deploy-db-1:tmp/biosamples.json
	docker cp cohorts.json deploy-db-1:tmp/cohorts.json
	docker cp datasets.json deploy-db-1:tmp/datasets.json
	docker cp genomicVariations.json deploy-db-1:tmp/genomicVariations.json
	docker cp individuals.json deploy-db-1:tmp/individuals.json
	docker cp runs.json deploy-db-1:tmp/runs.json
	docker cp filtering_terms.json deploy-db-1:tmp/filtering_terms.json
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/datasets.json --collection datasets
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/individuals.json --collection individuals
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/cohorts.json --collection cohorts
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/analyses.json --collection analyses
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/biosamples.json --collection biosamples
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/runs.json --collection runs
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/genomicVariations.json --collection genomicVariations
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/filtering_terms.json --collection filtering_terms
	cd /data/vault/bio-scratch/arnau/beacon/data/tools-v2/rd-connect/json
	docker cp analyses.json deploy-db-1:tmp/analyses.json
	docker cp biosamples.json deploy-db-1:tmp/biosamples.json
	docker cp cohorts.json deploy-db-1:tmp/cohorts.json
	docker cp datasets.json deploy-db-1:tmp/datasets.json
	docker cp genomicVariations_id.json deploy-db-1:tmp/genomicVariations.json
	docker cp individuals.json deploy-db-1:tmp/individuals.json
	docker cp runs.json deploy-db-1:tmp/runs.json
	docker cp filtering_terms.json deploy-db-1:tmp/filtering_terms.json
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/datasets.json --collection datasets
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/individuals.json --collection individuals
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/cohorts.json --collection cohorts
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/analyses.json --collection analyses
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/biosamples.json --collection biosamples
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/runs.json --collection runs
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/genomicVariations.json --collection genomicVariations
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/filtering_terms.json --collection filtering_terms
	docker exec beacon python beacon/reindex.py
	docker exec beacon python beacon/db/extract_filtering_terms.py
	cd .../frontend
	cp docker-compose...
	docker-compose up -d --build beacon