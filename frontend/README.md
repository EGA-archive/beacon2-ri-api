## Deploy

Use the deployment for all the containers for beacon to also deploy the UI [Deployment](https://github.com/EGA-archive/beacon2-ri-api/blob/develop/deploy/README.md). You will find it running in http://localhost:3000

## Instructions on how to configure the Beacon User Interface
 
Please first create a .env file inside the frontend folder so that you can modify some variables as follows:

```bash
REACT_APP_CLIENT_ID="ID of your LS Login"
REACT_APP_CLIENT_SECRET="password of your LS Login"
```

Take into account that the above file will not be copied to GitHub as it contains keys and for security reasons it should ignored.

Then please edit the file config.json, which can be found inside folder [frontend/src](https://github.com/EGA-archive/beacon2-ri-api/blob/develop/frontend/src/config.json). You need to decide where you want the UI to point to when making requests. Find below an example:

 ```bash
{
   "API_URL": "https://yourAPIdomain.com/beacon-network/v2.0.0",
   "REDIRECT_URL": "https://yourUIdomain.com",
   "KEYCLOAK_URL": "https://yourKEYCLOAKdomain.com"
 }
```