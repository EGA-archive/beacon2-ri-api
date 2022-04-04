import json
import argparse
from pymongo.mongo_client import MongoClient

entities = ["analyses", "biosamples", "cohorts", "datasets", "genomicVariations", "individuals", "runs"]

def main():
    parser = argparse.ArgumentParser("JSON MongoDB Loader")

    parser.add_argument("--db", dest="db", action="store", help="Database URI", required=True)
    parser.add_argument("--files", dest="files", action="store", help="JSON Files path", required=True, nargs='+')
    parser.add_argument("--collection", dest="collection", action="store", help="Collection to store the data", required=True, choices=entities)
    
    args = parser.parse_args()

    print(args.files, "->", args.db, "[", args.collection, "]")

    all_instances = []

    for file in args.files:
        with open(file, 'r') as json_file:
            data = json.load(json_file)
            if isinstance(data, dict):
                print("Loading multiple files with one instance each")
                all_instances.append(data)
            else:
                print("Loading only one file with multiple instances")
                all_instances = data
                break
    
    client = MongoClient(args.db)
    client.beacon.get_collection(args.collection).insert_many(all_instances)
    print("DONE!")

if __name__ == "__main__":
    main()
