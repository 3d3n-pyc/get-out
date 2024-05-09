## Qu'est ce que c'est ?

Ce script permet de bannir les utilisateurs d'un serveur à partir d'un robot discord possédant la permission de bannir. Il est configurable et possède une belle interface !

## Installation

- Installer [Python](https://www.python.org/downloads/)

### Automatique

- Lancer le start.cmd

### Manuel

- Installer les modules du fichier [requirements](requirements.txt) : `python -m pip install -r requirements.txt`
- Lancer le [script python](main.py)

## Configuration

### Comment obtenir l'id de l'application ?

- Aller sur [Discord Developer Portal](https://discord.com/developers/applications)
- Aller sur l'application du bot
- Copier le `APPLICATION ID`

### Comment obtenir le token ?

- Aller sur [Discord Developer Portal](https://discord.com/developers/applications)
- Aller sur l'application du bot
- Cliquer sur `Bot`
- Cliquer sur `Reset Token`
- Copier le `Token`

### Comment activer les intents

- Aller sur [Discord Developer Portal](https://discord.com/developers/applications)
- Aller sur l'application du bot
- Cliquer sur `Bot`
- Descendre jusque `Privileged Gateway Intents`
- Cocher `PRESENCE INTENT`, `SERVER MEMBERS INTENT`, et `MESSAGE CONTENT INTENT`

### Comment copier l'id d'un serveur discord

- Suivez les étapes sur [cet article](https://support.discord.com/hc/fr/articles/206346498-O%C3%B9-trouver-l-ID-de-mon-compte-utilisateur-serveur-message)

## Mets une étoile, ça me soutient énormément ! 😉