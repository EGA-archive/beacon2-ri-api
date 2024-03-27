# Beacon v2.x

<!-- [![Testsuite](https://github.com/EGA-archive/beacon-2.x/workflows/Testsuite/badge.svg)](https://github.com/EGA-archive/beacon-2.x/actions) -->

This repository is an implementation of the [Beacon v2.0 Model](https://github.com/ga4gh-beacon/beacon-v2-Models) and contains:

* The (Python 3.9+) [source code for beacon](beacon),
* A MongoDB database with sample data to demo the capabilities of the Beacon API.
* AAI and LS-AAI integrated.


> [Local deployment instructions](deploy/README.md)

> [Frontend usage instructions](frontend/README.md)

### Managing AAI-LSAAI permissions

To give the right permissions for AAI you will need to set the permissions of the users inside permissions folder, within the [public_datasets.yml](permissions/public_datasets.yml), [registered_datasets.yml](permissions/registered_datasets.yml), [controlled_datasets.yml](permissions/controlled_datasets.yml) files, or run the beacon admin page that allows you to manage all the permissions in a friendly way and no need to open .yml files. Just start the UI, that will run in http://localhost:8010, by executing this command from the deploy folder after the containers are up and running:
```bash
docker exec beacon-permissions bash permissions/permissions-ui/start.sh
```
Please, bear in mind that the name of the user has to be the same that you used when creating the user in LS or in IDP, whatever the AAI method you are working with.
To give a user a certain type of response for their queries, please modify this file [response_type.yml](https://github.com/EGA-archive/beacon2-ri-api/blob/master/beacon/request/response_type.yml) adding the maximum type of response you want to allow every user.

Also, you will need to edit the file [conf.py](beacon/conf.py) and introduce the domain where your keycloak is being hosted inside **idp_user_info** and the issuer you trust for your token inside **idp_issuer**. In case you want to run your local container, use this configuration:
```bash
idp_issuer='https://beacon-network-demo2.ega-archive.org/auth/realms/Beacon'
idp_user_info = 'https://beacon-network-demo2.ega-archive.org/auth/realms/Beacon/protocol/openid-connect/userinfo'
lsaai_issuer='https://login.elixir-czech.org/oidc/'
lsaai_user_info = 'https://login.elixir-czech.org/oidc/userinfo'
```

Also, inside the folder permissions, before building your permissions container, you will need to create an .env file and add the CLIENT_ID for your LSAAI or Keycloak or both, with these same variable names:
```bash
LSAAI_CLIENT_ID='your_lsaai_client_id'
KEYCLOAK_CLIENT_ID='your_keycloak_client_id'
```
When you have your access token, pass it in a header with **Authorization: Bearer** in your POST request to get your answers. This token works coming from either from LS AAI or from keycloak (idp container).

### Beacon security system

![Beacon security](https://github.com/EGA-archive/beacon2-ri-api/blob/develop/deploy/beacon_security.png?raw=true)

### Version notes

* Fusions (`mateName`) are not supported.


### Acknowlegments

We thank the [CSC Finland](https://www.csc.fi/) team for their
contribution with a [python implementing of version
1](https://github.com/CSCfi/beacon-python). They, in turn, got help
from members of [NBIS](https://nbis.se/) and
[DDBJ](https://www.ddbj.nig.ac.jp).
