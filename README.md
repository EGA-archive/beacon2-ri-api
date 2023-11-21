# Beacon v2.x

<!-- [![Testsuite](https://github.com/EGA-archive/beacon-2.x/workflows/Testsuite/badge.svg)](https://github.com/EGA-archive/beacon-2.x/actions) -->

This repository is an implementation of the [Beacon v2.0 Model](https://github.com/ga4gh-beacon/beacon-v2-Models) and contains:

* The (Python 3.9+) [source code for beacon](beacon),
* A MongoDB database with sample data to demo the capabilities of the Beacon API.
* AAI and LS-AAI integrated.


> [Local deployment instructions](deploy/README.md)

### Managing AAI-LSAAI permissions

To give the right permissions for AAI you will need to set the permissions of the users inside permissions folder, within the [public_datasets.yml](permissions/public_datasets.yml), [registered_datasets.yml](permissions/registered_datasets.yml), [controlled_datasets.yml](permissions/controlled_datasets.yml) files, or run the beacon admin page that allows you to manage all the permissions in a friendly way and no need to open .yml files. Just start the UI, that will run in http://localhost:8010, by executing this command from the deploy folder after the containers are up and running:
```bash
docker exec beacon-permissions bash permissions/permissions-ui/start.sh
```
Please, bear in mind that the name of the user has to be the same that you used when creating the user in LS or in IDP, whatever the AAI method you are working with.

Also, you will need to edit the file [conf.py](beacon/conf.py) and introduce the domain where your keycloak is being hosted inside **ldp_user_info** and the issuers you trust for your token inside **trusted_issuers**. In case you want to run your local container, use this configuration:
```bash
idp_user_info = 'http://idp:8080/auth/realms/Beacon/protocol/openid-connect/userinfo'
lsaai_user_info = 'https://login.elixir-czech.org/oidc/userinfo'
trusted_issuers = ['http://idp:8080/auth/realms/Beacon', 'https://login.elixir-czech.org/oidc/']
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
