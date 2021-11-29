
import os
import sys
import json

def clean(path):
    os.system("json-dereference -s {} -o {}".format(path, path))

def main():
    for root, dirs, files in os.walk(sys.argv[1], topdown=False):
        for name in files:
            if name.endswith("json") and not name.endswith("endpoints.json"):
                print(os.path.join(root, name))
                clean(os.path.join(root, name))

if __name__ == "__main__":
    main()