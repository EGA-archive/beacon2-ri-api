# Ontologies

> This step might require a bit of tinkering since some ontologies used in the dummy data will fail to loaded. I recommend skipping this step unless you know what you are doing.

You can automatically fetch the ontologies that the database is using with the following script:

```bash
# Install the dependencies
pip3 install pymongo tqdm

# From the deploy/ directory
python3 fetch_ontologies.py
```
