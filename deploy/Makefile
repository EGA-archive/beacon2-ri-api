build:
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/belcovid2/json/genomicVariations2.json mongoega:tmp/genomicVariations.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/belcovid2/json/biosamples.json mongoega:tmp/biosamples.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/belcovid2/json/cohorts.json mongoega:tmp/cohorts.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/belcovid2/json/datasets.json mongoega:tmp/datasets.json
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/individuals_modified/bracovid_individuals_modified.json mongoega:tmp/individuals.json
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