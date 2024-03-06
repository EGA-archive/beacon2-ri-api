#!/bin/bash 

echo "Keycloak"

# cd /opt/keycloak/conf/certs
# ./gencerts.sh

#/opt/keycloak/bin/kc.sh import --file=/tmp/beacon-realm.json --optimized
/opt/keycloak/bin/kc.sh build
/opt/keycloak/bin/kc.sh show-config
/opt/keycloak/bin/kc.sh start --optimized
