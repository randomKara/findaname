FROM quay.io/keycloak/keycloak:26.1.4

ENV KC_HEALTH_ENABLED=true
ENV KC_METRICS_ENABLED=true
ENV KC_FEATURES=token-exchange
ENV KC_DB=dev-file
ENV KC_HTTPS_CERTIFICATE_FILE=/opt/keycloak/certs/cert.pem
ENV KC_HTTPS_CERTIFICATE_KEY_FILE=/opt/keycloak/certs/key.pem
ENV KC_HOSTNAME=keycloak
ENV KC_HOSTNAME_STRICT=false
ENV KC_PROXY=edge
ENV KC_HTTP_ENABLED=true
ENV KC_HTTPS_PORT=8443

# Copier le fichier realm.json et les certificats
COPY realm.json /opt/keycloak/data/import/
COPY certs/ /opt/keycloak/certs/

# S'assurer que les fichiers de certificat ont les bonnes permissions
USER root
RUN chmod 644 /opt/keycloak/certs/cert.pem && \
    chmod 644 /opt/keycloak/certs/key.pem && \
    chown -R keycloak:keycloak /opt/keycloak/certs
USER keycloak

ENTRYPOINT ["/opt/keycloak/bin/kc.sh", "start-dev", "--import-realm"]
