build:
	docker cp /data/vault/bio-scratch/arnau/beacon/data/tools-v2/hgi/hgi_full/belcovid2/json/genomicVariations2.json mongoega:tmp/genomicVariations.json
	docker exec mongoega mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27020/beacon?authSource=admin" --file /tmp/genomicVariations.json --collection genomicVariations