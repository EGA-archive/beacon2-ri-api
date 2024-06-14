build:
	docker-compose up -d --build beaconega permissionsega
	sleep 10
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/belcovid2/json/genomicVariations2.json mongoega:tmp/genomicVariations.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/belcovid2/json/biosamples.json mongoega:tmp/biosamples.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/belcovid2/json/cohorts.json mongoega:tmp/cohorts.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/belcovid2/json/datasets.json mongoega:tmp/datasets.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/individuals_modified/belcovid2_individuals_modified.json mongoega:tmp/individuals.json
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/datasets.json --collection datasets
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/individuals.json --collection individuals
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/cohorts.json --collection cohorts
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/biosamples.json --collection biosamples
	docker cp /data/vault/bio-scratch/arnau/beacon/beacon2-ri-tools-v2_test_anot/tcga-coad/analyses.json mongoega:tmp/analyses.json
	docker cp /data/vault/bio-scratch/arnau/beacon/beacon2-ri-tools-v2_test_anot/tcga-coad/biosamples.json mongoega:tmp/biosamples.json
	docker cp /data/vault/bio-scratch/arnau/beacon/beacon2-ri-tools-v2_test_anot/tcga-coad/cohorts.json mongoega:tmp/cohorts.json
	docker cp /data/vault/bio-scratch/arnau/beacon/beacon2-ri-tools-v2_test_anot/tcga-coad/datasets.json mongoega:tmp/datasets.json
	docker cp /data/vault/bio-scratch/arnau/beacon/beacon2-ri-tools-v2_test_anot/tcga-coad/genomicVariations.json mongoega:tmp/genomicVariations.json
	docker cp /data/vault/bio-scratch/arnau/beacon/beacon2-ri-tools-v2_test_anot/tcga-coad/individuals.json mongoega:tmp/individuals.json
	docker cp /data/vault/bio-scratch/arnau/beacon/beacon2-ri-tools-v2_test_anot/tcga-coad/runs.json mongoega:tmp/runs.json
	docker cp /data/vault/bio-scratch/arnau/beacon/beacon2-ri-tools-v2_test_anot/tcga-coad/filtering_terms.json mongoega:tmp/filtering_terms.json
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/datasets.json --collection datasets
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/individuals.json --collection individuals
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/cohorts.json --collection cohorts
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/analyses.json --collection analyses
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/biosamples.json --collection biosamples
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/runs.json --collection runs
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/genomicVariations.json --collection genomicVariations
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/filtering_terms.json --collection filtering_terms
	docker exec beaconega python beacon/reindex.py
	docker exec beaconega python beacon/db/extract_filtering_terms.py	