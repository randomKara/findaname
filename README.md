# Démonstration d'Authentification avec Keycloak et FIDO

Ce projet est une démonstration d'un système d'authentification utilisant Keycloak comme fournisseur d'identité et différentes méthodes d'authentification, incluant les mots de passe traditionnels, les Passkeys et les clés de sécurité FIDO USB.

## Architecture

Le système est composé de plusieurs services Docker interconnectés :

- **Keycloak** : Serveur d'identité et d'authentification
- **OpenLDAP** : Annuaire utilisateurs (backend pour Keycloak)
- **Flask App** : Application web utilisant l'authentification par mot de passe
- **Flask App Passkey** : Application web utilisant l'authentification par Passkey
- **Flask App FIDO** : Application web utilisant l'authentification par clé FIDO USB

## Prérequis

- Docker et Docker Compose
- Un navigateur moderne compatible WebAuthn (Chrome, Firefox, Edge, Safari)
- Une clé de sécurité FIDO pour la démonstration de l'authentification par clé USB
- Système Debian 12 (Bookworm) ou compatible

## Installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/randomKara/keycloak-fido-demo.git
   cd keycloak-fido-demo
   ```

2. Configurez la résolution DNS pour le proxy (obligatoire) :
   ```bash
   sudo sed -i '2i nameserver 172.29.0.1' /etc/resolv.conf
   ```
   **Note importante** : Cette commande est obligatoire pour l'ajout du proxy de façon temporaire. Elle permet aux conteneurs de communiquer correctement entre eux.

3. Démarrez les services :
   ```bash
   docker compose up -d
   ```
   Enlever le `-d` pour voir tout les logs.

4. Attendre que tous les services démarrent (Keycloak peut prendre jusqu'à 1 minute) :
   ```bash
   docker compose logs -f keycloak
   ```

## Utilisation

### Accès aux applications

- **Application OTP** : http://localhost:5000
- **Application Passkey** : http://localhost:5001
- **Application FIDO** : http://localhost:5002

### Interface d'administration Keycloak

- URL : https://localhost:8443/admin
- Identifiants : admin / admin

### Inscription et gestion des clés de sécurité

1. Connectez-vous à l'une des applications (identifiants: user1/user1 | user2/user2 | user3/user3 )
2. Accédez à la gestion de votre compte via le lien "Gérer mes clés FIDO" ou "Gérer mes passkeys" (Afin de verifier que vous êtes bien connecté avec le bon compte)
3. Dans l'interface utilisateur de Keycloak, allez dans "Sign in" > "Security keys" pour enregistrer une nouvelle clé

## Configuration de la clé FIDO USB

Pour utiliser une clé FIDO USB avec l'application Flask-App-FIDO, aucune installation spécifique n'est nécessaire sur le PC hôte. Les navigateurs modernes et Debian 12 reconnaissent nativement les clés FIDO2/U2F.

Si vous rencontrez des problèmes de détection de la clé, vous pouvez effectuer les vérifications suivantes :

1. Ajoutez votre utilisateur au groupe plugdev :
   ```bash
   sudo usermod -a -G plugdev $USER
   ```
   Puis redémarrez votre session.

2. Installez les règles udev pour les clés FIDO :
   ```bash
   sudo apt install libu2f-udev
   ```

## Structure du projet

```
keycloak-fido-demo/
├── docker-compose.yml
├── flask-app/              # Application OTP
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── templates/
├── flask-app-passkey/      # Application avec Passkey
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── templates/
├── flask-app-fido/         # Application avec clé FIDO USB
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── templates/
├── keycloak/
│   ├── certs/
│   ├── Dockerfile
│   └── realm.json
└── ldap/
    └── ...
```

## Fonctionnement

Chaque application Flask redirrige les utilisateurs vers Keycloak pour l'authentification. Selon l'application, Keycloak utilise un flux d'authentification différent :

- **flask-app** : Authentification standard par mot de passe et OTPs
- **flask-app-passkey** : Authentification par Passkey (WebAuthn)
- **flask-app-fido** : Authentification par clé de sécurité FIDO USB (WebAuthn)

Les deux dernières applications utilisent le même flux d'authentification WebAuthn configuré dans Keycloak, mais avec des clients différents.

## Dépannage

### Problèmes de connexion

- Vérifiez que les certificats auto-signés sont acceptés par votre navigateur
- Assurez-vous que la résolution DNS est correctement configurée avec la commande fournie
- Consultez les logs de Keycloak pour les erreurs d'authentification :
  ```bash
  docker-compose logs keycloak
  ```

### Problèmes avec les clés FIDO

- Vérifiez la compatibilité de votre navigateur avec WebAuthn sur https://webauthn.io
- Assurez-vous que votre clé FIDO est correctement détectée par votre système
- Vérifiez que la clé est bien enregistrée dans votre compte Keycloak

