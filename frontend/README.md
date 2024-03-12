## Deploy

Use the deployment for all the containers for beacon to also deploy the UI [Deployment](https://github.com/EGA-archive/beacon2-ri-api/blob/develop/deploy/README.md). You will find it running in http://localhost:3000

## Instructions on how to configure the Beacon User Interface
 
Please first create a .env file inside the frontend folder so that you can modify some variables. Take into account that the file below will not be copied to GitHub as it contains keys and for security reasons it should ignored: 

```bash
REACT_APP_CLIENT_ID="ID of your LS Login"
REACT_APP_CLIENT_SECRET="password of your LS Login"
REACT_APP_KEYCLOAK_CLIENT_SECRET="password of your Keycloak login"
```

You will need to have created your Life Science and Keycloak environments before.

Tip: for Life Science environment, please first [create a user](https://lifescience-ri.eu/ls-login/users/how-to-get-and-use-life-science-id.html) . 
After that you will need to register a service registry in order to be able to administrate your logins. Please go [here](https://services.aai.lifescience-ri.eu/spreg/) and ask for a New Service - type OIDC -.


Then please edit the file config.json, which can be found inside folder [frontend/src](https://github.com/EGA-archive/beacon2-ri-api/blob/develop/frontend/src/config.json). You need to decide where you want the UI to point to when making requests. Find below an example:

 ```bash
{
   "API_URL": "https://yourAPIdomain.com/beacon-network/v2.0.0",
   "REDIRECT_URL": "https://yourUIdomain.com",
   "KEYCLOAK_URL": "https://yourKEYCLOAKdomain.com"
 }
```

Note that in the frontend folder you will find a file called .gitignore with the list of all files that need to be ignored.
