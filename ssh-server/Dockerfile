FROM ubuntu:22.04

# Installation des paquets nécessaires
RUN apt-get update && apt-get install -y \
    openssh-server \
    libnss-ldap \
    libpam-ldap \
    nscd \
    ldap-utils \
    && rm -rf /var/lib/apt/lists/*

# Configuration de PAM pour utiliser LDAP
RUN echo "auth required pam_ldap.so" >> /etc/pam.d/common-auth \
    && echo "account required pam_ldap.so" >> /etc/pam.d/common-account \
    && echo "password required pam_ldap.so" >> /etc/pam.d/common-password \
    && echo "session required pam_ldap.so" >> /etc/pam.d/common-session

# Configuration de NSS pour utiliser LDAP
RUN echo "passwd: ldap files" >> /etc/nsswitch.conf \
    && echo "group: ldap files" >> /etc/nsswitch.conf \
    && echo "shadow: ldap files" >> /etc/nsswitch.conf

# Configuration de LDAP
RUN echo "uri ldap://openldap:389" > /etc/ldap.conf \
    && echo "base dc=mondomaine,dc=com" >> /etc/ldap.conf \
    && echo "binddn cn=admin,dc=mondomaine,dc=com" >> /etc/ldap.conf \
    && echo "bindpw admin" >> /etc/ldap.conf \
    && echo "ssl no" >> /etc/ldap.conf \
    && echo "tls no" >> /etc/ldap.conf

# Configuration SSH
RUN mkdir /var/run/sshd \
    && echo "PermitRootLogin no" >> /etc/ssh/sshd_config \
    && echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config \
    && echo "UsePAM yes" >> /etc/ssh/sshd_config

# Exposition du port SSH
EXPOSE 22

# Démarrage des services
CMD ["/usr/sbin/sshd", "-D"] 