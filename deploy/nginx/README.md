
#### Config
The common name (CN) SHOULD match the hostname (or FQDN) of the beacon / server
certs/self_cert.conf

The `server_name` SHOULD also match hostname or FQDN.
etc/nginx/conf.d:
  - permissions.conf
  - beacon.conf
  - frontend.conf

#### Build container:
`docker build -t egarchive/beacon-revprox:1.0 .`

#### Run container:
`docker run --hostname beacon-revprox --name beacon-revprox --network my-app-network --network deploy_default -p 5050:5050 -p 5051:5051 -p 3000:3000 -it egarchive/beacon-revprox:1.0`

#### Re-spin the beacon containers without host port mappings 
`docker compose -f docker-compose.yml -f dc-remove-host-port-mappings.yml up -d`

