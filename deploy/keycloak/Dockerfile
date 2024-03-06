FROM ${B2RI_IDP_IMAGE:-keycloak/keycloak:24.0.1-0}

RUN mkdir -p /opt/keycloak/conf/certs 
RUN mkdir -p /opt/keycloak/data/import

USER root
COPY --chown=keycloak keycloak/beacon-realm.json      /opt/keycloak/data/import/
COPY --chown=keycloak keycloak/keycloak-entrypoint.sh /opt/keycloak/bin/
COPY --chown=keycloak keycloak/keycloak.conf          /opt/keycloak/conf/
COPY --chown=keycloak certs                           /opt/keycloak/conf/certs/

USER keycloak
RUN /opt/keycloak/bin/kc.sh build

ENTRYPOINT ["/opt/keycloak/bin/keycloak-entrypoint.sh"]
