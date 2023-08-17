# Beacon v2.x

<!-- [![Testsuite](https://github.com/EGA-archive/beacon-2.x/workflows/Testsuite/badge.svg)](https://github.com/EGA-archive/beacon-2.x/actions) -->

This repository is an implementation of the [Beacon v2.0 Model](https://github.com/ga4gh-beacon/beacon-v2-Models) and contains:

* The (Python 3.9+) [source code for beacon](beacon),
* A MongoDB database with sample data to demo the capabilities of the Beacon API.
* AAI and LS-AAI integrated. For LS-AAI, gdi ls aai mock repository is required to be up and running in another docker compose service, and then you will need to create this external network:
```bash
docker network create my-app-network
```

> [Local deployment instructions](deploy/README.md)

### Managing AAI-LSAAI permissions

To give the right permissions for AAI you will need to set the permissions of the users inside permissions folder, within the [permissions.yml](permissions/permissions.yml) file. 
Please, bear in mind that the name of the user has to be the same that you used when creating the user in LS or in IDP, whatever the AAI method you are working with.
Furthermore, if you are using LS-AAI method, you will need to get the authorization code following LS-AAI authorization flow method with a browser (for example http://localhost:8080/oidc/auth/authorize?response_type=code&client_id=app-123) and then pass this code via a POST request to get the authorization token. For example:
```bash
curl --location --request POST 'http://localhost:8080/oidc/token' \--header 'Content-Type: application/x-www-form-urlencoded' \--data-urlencode 'grant_type=authorization_code' \--data-urlencode 'code=pasteyourcodefrombrowserhere' \--data-urlencode 'client_id=app-123' \--data-urlencode 'client_secret=secret_value' \--data-urlencode 'scope=openid' \
--data-urlencode 'requested_token_type=urn:ietf:params:oauth:token-type:refresh_token'
```
When you have your authorization token, pass it in a header in your POST request to get your answers.

### Making real LS AAI work

This repository is made to work with mock LS AAI. It still has not been developed to work with real LS AAI. However, real LS AAI should inmediately work with only a couple of changes. In order to make it work with real LS AAI, please change the mock for the real LS AAI endpoints in the auth.py file inside permissions folder:
```bash
idp_user_info  = 'http://ls-aai-mock:8080/oidc/userinfo'
idp_introspection = 'http://ls-aai-mock:8080/oidc/introspect'
```
Then, if the user is created in LS AAI, just add its permissions in permissions.yml file and you should have a beacon connecting to real LS AAI.

### Version notes

* Fusions (`mateName`) are not supported.


### Acknowlegments

We thank the [CSC Finland](https://www.csc.fi/) team for their
contribution with a [python implementing of version
1](https://github.com/CSCfi/beacon-python). They, in turn, got help
from members of [NBIS](https://nbis.se/) and
[DDBJ](https://www.ddbj.nig.ac.jp).
