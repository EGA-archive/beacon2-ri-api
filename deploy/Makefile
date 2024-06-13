build:
	docker-compose up -d --build beaconega permissionsega
	sleep 10
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/bracovid/json/BRACOVID_genomicVariations.json mongoega:tmp/genomicVariations.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/bracovid/json/biosamples.json mongoega:tmp/biosamples.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/bracovid/json/cohorts.json mongoega:tmp/cohorts.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/bracovid/json/datasets.json mongoega:tmp/datasets.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/individuals_modified/bracovid_individuals_modified.json mongoega:tmp/individuals.json
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/datasets.json --collection datasets
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/individuals.json --collection individuals
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/cohorts.json --collection cohorts
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/biosamples.json --collection biosamples
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/genomicVariations.json --collection genomicVariations
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/gen-covid/json/GEN-COVID_genomicVariations.json mongoega:tmp/genomicVariations.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/gen-covid/json/biosamples.json mongoega:tmp/biosamples.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/gen-covid/json/cohorts.json mongoega:tmp/cohorts.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/gen-covid/json/datasets.json mongoega:tmp/datasets.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/individuals_modified/gen-covid_individuals_modified.json mongoega:tmp/individuals.json
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/datasets.json --collection datasets
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/individuals.json --collection individuals
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/cohorts.json --collection cohorts
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/biosamples.json --collection biosamples
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/genomicVariations.json --collection genomicVariations	
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/hostage_1/json/Hostage_1_genomicVariations.json mongoega:tmp/genomicVariations.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/hostage_1/json/biosamples.json mongoega:tmp/biosamples.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/hostage_1/json/cohorts.json mongoega:tmp/cohorts.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/hostage_1/json/datasets.json mongoega:tmp/datasets.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/individuals_modified/hostage_1_individuals_modified.json mongoega:tmp/individuals.json
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/datasets.json --collection datasets
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/individuals.json --collection individuals
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/cohorts.json --collection cohorts
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/biosamples.json --collection biosamples
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/genomicVariations.json --collection genomicVariations
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/hostage_2/json/Hostage_2_genomicVariations.json mongoega:tmp/genomicVariations.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/hostage_2/json/biosamples.json mongoega:tmp/biosamples.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/hostage_2/json/cohorts.json mongoega:tmp/cohorts.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/hostage_2/json/datasets.json mongoega:tmp/datasets.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/individuals_modified/hostage_2_individuals_modified.json mongoega:tmp/individuals.json
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/datasets.json --collection datasets
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/individuals.json --collection individuals
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/cohorts.json --collection cohorts
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/biosamples.json --collection biosamples
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/genomicVariations.json --collection genomicVariations
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/hostage_3/json/Hostage_3_genomicVariations.json mongoega:tmp/genomicVariations.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/hostage_3/json/biosamples.json mongoega:tmp/biosamples.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/hostage_3/json/cohorts.json mongoega:tmp/cohorts.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/hostage_3/json/datasets.json mongoega:tmp/datasets.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/individuals_modified/hostage_3_individuals_modified.json mongoega:tmp/individuals.json
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/datasets.json --collection datasets
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/individuals.json --collection individuals
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/cohorts.json --collection cohorts
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/biosamples.json --collection biosamples
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/genomicVariations.json --collection genomicVariations
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/hostage_4/json/Hostage_4_genomicVariations.json mongoega:tmp/genomicVariations.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/hostage_4/json/biosamples.json mongoega:tmp/biosamples.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/hostage_4/json/cohorts.json mongoega:tmp/cohorts.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/hostage_4/json/datasets.json mongoega:tmp/datasets.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/individuals_modified/hostage_4_individuals_modified.json mongoega:tmp/individuals.json
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/datasets.json --collection datasets
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/individuals.json --collection individuals
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/cohorts.json --collection cohorts
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/biosamples.json --collection biosamples
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/genomicVariations.json --collection genomicVariations	
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/inmungen_cov2/json/INMUNGEN_CoV2_genomicVariations.json mongoega:tmp/genomicVariations.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/inmungen_cov2/json/biosamples.json mongoega:tmp/biosamples.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/inmungen_cov2/json/cohorts.json mongoega:tmp/cohorts.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/inmungen_cov2/json/datasets.json mongoega:tmp/datasets.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/individuals_modified/inmungen_cov2_individuals_modified.json mongoega:tmp/individuals.json
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/datasets.json --collection datasets
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/individuals.json --collection individuals
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/cohorts.json --collection cohorts
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/biosamples.json --collection biosamples
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/genomicVariations.json --collection genomicVariations	
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/spgrx/json/SPGRX_genomicVariations.json mongoega:tmp/genomicVariations.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/spgrx/json/biosamples.json mongoega:tmp/biosamples.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/spgrx/json/cohorts.json mongoega:tmp/cohorts.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/spgrx/json/datasets.json mongoega:tmp/datasets.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/individuals_modified/spgrx_individuals_modified.json mongoega:tmp/individuals.json
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/datasets.json --collection datasets
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/individuals.json --collection individuals
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/cohorts.json --collection cohorts
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/biosamples.json --collection biosamples
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/genomicVariations.json --collection genomicVariations
	docker exec beaconega python beacon/reindex.py
