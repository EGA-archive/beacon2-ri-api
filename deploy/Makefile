build:
	docker cp /Users/olopezdoriga/Desktop/gen-covid/biosamples.json rimongo:tmp/biosamples.json
	docker cp /Users/olopezdoriga/Desktop/gen-covid/datasets.json rimongo:tmp/datasets.json
	docker cp /Users/olopezdoriga/Desktop/gen-covid/genomicVariations.json rimongo:tmp/genomicVariations.json
	docker cp /Users/olopezdoriga/Desktop/gen-covid/individuals.json rimongo:tmp/individuals.json
	docker exec rimongo mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/datasets.json --collection datasets
	docker exec rimongo mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/individuals.json --collection individuals
	docker exec rimongo mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/cohorts.json --collection cohorts
	docker exec rimongo mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/biosamples.json --collection biosamples
	docker exec rimongo mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/genomicVariations.json --collection genomicVariations
	docker cp /Users/olopezdoriga/Desktop/TCGA/biosamples.json rimongo:tmp/biosamples.json
	docker cp /Users/olopezdoriga/Desktop/TCGA/cohorts.json rimongo:tmp/cohorts.json
	docker cp /Users/olopezdoriga/Desktop/TCGA/datasets.json rimongo:tmp/datasets.json
	docker cp /Users/olopezdoriga/Desktop/TCGA/genomicVariations.json rimongo:tmp/genomicVariations.json
	docker cp /Users/olopezdoriga/Desktop/TCGA/individuals.json rimongo:tmp/individuals.json
	docker exec rimongo mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/datasets.json --collection datasets
	docker exec rimongo mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/individuals.json --collection individuals
	docker exec rimongo mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/cohorts.json --collection cohorts
	docker exec rimongo mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/biosamples.json --collection biosamples
	docker exec rimongo mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/genomicVariations.json --collection genomicVariations
	docker exec beacon python beacon/reindex.py