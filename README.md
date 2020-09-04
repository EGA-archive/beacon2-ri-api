# Beacon v2.x

[![Testsuite](https://github.com/EGA-archive/beacon-2.x/workflows/Testsuite/badge.svg)](https://github.com/EGA-archive/beacon-2.x/actions)

This repository is an implementation of the [Beacon v2.0 specification](https://github.com/ga4gh-beacon/specification-v2) and contains:

* the (Python 3.7+) [source code for Beacon version 2.x](beacon),
* instructions for a [local deployment](deploy) (using docker and docker-compose),
* a set of [templates for a Beacon UI](ui).


# Structure




# Database

Here you can find a diagram of the database schema:
![Database schema diagram](beacon_db_schema_v2.0.png)

This schema also includes several functions which manage everything related to querying the data and are called from the Python code.  

These functions are:
* `query_gvariants`: queries the `variant_table`.
* `query_individuals`: queries the `individual_table`.
* `query_samples`: queries the `sample_table`.

There are also the following helper functions used by the previous ones:
* `add_where_clause_conditions`: prepares the conditions that will be in the `WHERE` clause.
* `find_format`: some fields are formatted as JSON by the main function. This function finds the schema which has to be used to build this JSON.  
* `parse_filters`: prepares the filters' values so they can be added to the query.


# Deployment

See instructions in [/deploy](deploy).


# Version notes

* Structural variants (`variantType`) are not supported.
* Fuzzy matches (`startMin`, `startMax`, `endMin`, `endMax`) are not supported.
* Fusions (`mateName`) are not supported.


# Acknowlegments

We thank the [CSC Finland](https://www.csc.fi/) team for their
contribution with a [python implementing of version
1](https://github.com/CSCfi/beacon-python). They, in turn, got help
from members of [NBIS](https://nbis.se/) and
[DDBJ](https://www.ddbj.nig.ac.jp).


