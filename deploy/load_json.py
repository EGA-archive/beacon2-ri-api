import json
import argparse
from pymongo import MongoClient

entities = ["analyses", "biosamples", "cohorts", "datasets", "g_variants", "individuals", "runs"]

def main():
    parser = argparse.ArgumentParser("JSON MongoDB Loader")

    parser.add_argument("--db", dest="db", action="store", help="Database URI", required=True)
    parser.add_argument("--file", dest="file", action="store", help="JSON File path", required=True)
    parser.add_argument("--collection", dest="collection", action="store", help="Collection to store the data", required=True, choices=entities)
    
    args = parser.parse_args()

    print(args.file, "->", args.db, "[", args.collection, "]")

    with open(args.file, 'r') as json_file:
        data = json.load(json_file)
        client = MongoClient(args.db)
        client.beacon.get_collection(args.collection).insert_many(data)
        print("DONE!")

if __name__ == "__main__":
    main()
