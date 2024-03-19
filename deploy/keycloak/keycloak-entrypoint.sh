#!/bin/bash 

echo "Keycloak Entrypoint¦ StartUp"

/opt/keycloak/bin/kc.sh show-config
/opt/keycloak/bin/kc.sh start --optimized --import-realm --verbose
