build:
	docker-compose up -d --build
	sleep 10
	docker exec deploy-db-1 /bin/bash -c 'mongo beacon -u root -p example --authenticationDatabase admin --eval "db.filtering_terms.deleteMany({})"'
	docker exec deploy-db-1 /bin/bash -c 'mongo beacon -u root -p example --authenticationDatabase admin --eval "db.analyses.deleteMany({})"'
	docker exec deploy-db-1 /bin/bash -c 'mongo beacon -u root -p example --authenticationDatabase admin --eval "db.biosamples.deleteMany({})"'
	docker exec deploy-db-1 /bin/bash -c 'mongo beacon -u root -p example --authenticationDatabase admin --eval "db.cohorts.deleteMany({})"'
	docker exec deploy-db-1 /bin/bash -c 'mongo beacon -u root -p example --authenticationDatabase admin --eval "db.datasets.deleteMany({})"'
	docker exec deploy-db-1 /bin/bash -c 'mongo beacon -u root -p example --authenticationDatabase admin --eval "db.genomicVariations.deleteMany({})"'
	docker exec deploy-db-1 /bin/bash -c 'mongo beacon -u root -p example --authenticationDatabase admin --eval "db.individuals.deleteMany({})"'
	docker exec deploy-db-1 /bin/bash -c 'mongo beacon -u root -p example --authenticationDatabase admin --eval "db.runs.deleteMany({})"'
	docker cp /data/vault/bio-scratch/arnau/beacon/beacon2-ri-tools-v2_test_anot/analyses.json deploy-db-1:tmp/analyses.json
	docker cp /data/vault/bio-scratch/arnau/beacon/beacon2-ri-tools-v2_test_anot/biosamples.json deploy-db-1:tmp/biosamples.json
	docker cp /data/vault/bio-scratch/arnau/beacon/beacon2-ri-tools-v2_test_anot/cohorts.json deploy-db-1:tmp/cohorts.json
	docker cp /data/vault/bio-scratch/arnau/beacon/beacon2-ri-tools-v2_test_anot/datasets.json deploy-db-1:tmp/datasets.json
	docker cp /data/vault/bio-scratch/arnau/beacon/beacon2-ri-tools-v2_test_anot/genomicVariations.json deploy-db-1:tmp/genomicVariations.json
	docker cp /data/vault/bio-scratch/arnau/beacon/beacon2-ri-tools-v2_test_anot/individuals.json deploy-db-1:tmp/individuals.json
	docker cp /data/vault/bio-scratch/arnau/beacon/beacon2-ri-tools-v2_test_anot/runs.json deploy-db-1:tmp/runs.json
	docker cp /data/vault/bio-scratch/arnau/beacon/beacon2-ri-tools-v2_test_anot/filtering_terms.json deploy-db-1:tmp/filtering_terms.json
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/datasets.json --collection datasets
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/individuals.json --collection individuals
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/cohorts.json --collection cohorts
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/analyses.json --collection analyses
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/biosamples.json --collection biosamples
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/runs.json --collection runs
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/genomicVariations.json --collection genomicVariations
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/filtering_terms.json --collection filtering_terms
	docker cp data/analyses.json deploy-db-1:tmp/analyses.json
	docker cp data/biosamples.json deploy-db-1:tmp/biosamples.json
	docker cp data/cohorts.json deploy-db-1:tmp/cohorts.json
	docker cp data/datasets.json deploy-db-1:tmp/datasets.json
	docker cp data/genomicVariations.json deploy-db-1:tmp/genomicVariations.json
	docker cp data/individuals.json deploy-db-1:tmp/individuals.json
	docker cp data/runs.json deploy-db-1:tmp/runs.json
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/datasets.json --collection datasets
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/individuals.json --collection individuals
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/cohorts.json --collection cohorts
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/analyses.json --collection analyses
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/biosamples.json --collection biosamples
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/runs.json --collection runs
	docker exec deploy-db-1 mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/genomicVariations.json --collection genomicVariations
	docker exec beacon python beacon/reindex.py
	docker exec beacon python beacon/db/extract_filtering_terms.py