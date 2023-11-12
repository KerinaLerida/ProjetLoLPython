# Mon Dashboard

Bienvenue dans le projet de la création d'un dashboard sur le thème du jeu "League of Legends". Ce tableau de bord offre une visualisation interactive des données avec des fonctionnalités telles qu'un slider et listes déroulantes.

## User Guide

### Déploiement

Pour déployer le tableau de bord sur une autre machine, suivez ces étapes :

1. Clonez le dépôt : `git clone https://github.com/couton-keren-constantin-matthieu/mon-dashboard.git`
2. Installez les dépendances : `pip install -r requirements.txt`
3. Exécutez l'application : `python app.py`
4. Accédez au tableau de bord via votre navigateur à l'adresse : `http://127.0.0.1:8050/`

## Rapport d'Analyse

Le rapport d'analyse est disponible dans le fichier [Rapport_Analyse.pdf](Rapport_Analyse.pdf). Il met en avant les principales conclusions extraites des données.

## Developer Guide

### Architecture du Code

Le code est organisé comme suit :

- `app.py`: Point d'entrée de l'application.
- `prepa.py`: Prépare les données.
- `data/`: Stocke les données utilisées par le tableau de bord. (Fichiers CSV)

`prepa.py` : (+ en détails) 
####Chargement des donnnées :
    Fichier CSV des Pays :
        Le script charge les informations sur les pays à partir du fichier CSV curiexplore-pays.csv dans le répertoire data.
        Les informations incluent le nom, l'ISO2, les coordonnées géographiques, et d'autres attributs comme le groupe IDH.

    Serveurs Bonus :
        Le script définit un dictionnaire servers_bonus qui contient des informations spécifiques sur certains serveurs de League of Legends.
        Chaque serveur a un nom, une liste de pays associés, une relation vers une région spécifique (le cas échéant).
		
####Création de Dictionnaires :
    Dictionnaire pays_infos :
        Le script crée un dictionnaire pays_infos contenant des informations spécifiques sur chaque pays, extraites du fichier CSV.
        Les informations comprennent l'ISO2, les coordonnées géographiques, et les relations avec certaines régions (Amérique centrale et Caraïbes, Amérique du Nord).

    Association des Pays aux Serveurs :
        Le script associe chaque pays à un ou plusieurs serveurs en fonction de certaines relations, telles que la région d'Amérique centrale et des Caraïbes ou l'Amérique du Nord.
		
####Dictionnaire Final servers_countries :
    Structure du Dictionnaire :
        Le dictionnaire servers_countries regroupe les informations des serveurs et des pays.
        Chaque serveur ou pays a un nom, une liste de pays associés, et des coordonnées géographiques.

    Coordonnées Géographiques :
        Les coordonnées géographiques sont incluses pour chaque serveur et pays.
        Les coordonnées sont extraites du dictionnaire pays_infos pour les pays et calculées pour les serveurs à partir des coordonnées des pays associés.

####Utilisation du Dictionnaire :
    Accès aux Informations : 
        Les développeurs peuvent accéder aux informations d'un serveur ou d'un pays spécifique en utilisant son abréviation (ISO2 ou abréviation du serveur).

    Exemples d'Utilisation : (Commentés)
        Des exemples sont fournis dans le script pour montrer comment accéder à des informations spécifiques, comme les coordonnées d'un serveur ou d'un pays.

####Développement Futur :
	Ajout de Nouveaux Serveurs :
        Les développeurs peuvent ajouter de nouveaux serveurs en suivant le modèle défini dans le dictionnaire servers_bonus.

    Extension des Informations :
        Si de nouvelles informations sur les pays sont disponibles, les développeurs peuvent étendre le dictionnaire pays_infos pour inclure ces données.


`app.py` : (+ en détails) 
####Fonctionnalités principales :
    Chargement des Données :
        Les données sont chargées à partir de fichiers CSV présents dans le répertoire data. Chaque fichier CSV représente une saison.

    Prétraitement des Données :
        Les données sont prétraitées, notamment en ajustant les noms de colonnes, en convertissant les pourcentages en valeurs numériques, et en éliminant les données manquantes.

    Création de Graphiques :
        Deux types de graphiques sont générés : deux histogrammes et deux cartes choropleth pour visualiser les données géographiques des équipes.

    Interactivité :
        Le tableau de bord offre des fonctionnalités interactives, telles qu'un slider pour sélectionner la saison, des listes déroulantes pour choisir des caractéristiques spécifiques, et des cartes interactives.

####Strucutre du code :
	Chargement des Données :
        Utilisation d'os pour obtenir la liste des fichiers CSV dans le répertoire data.
        Création d'un dictionnaire data pour stocker les données de chaque saison.

    Prétraitement des Données :
        Utilisation de pandas pour lire et manipuler les données.
		
	Exceptions :
		Certains pays ont des exceptions dans les abréviations (iso2), nécessitant une gestion particulière.

    Création de Graphiques :
        Utilisation de Plotly Express pour générer des graphiques interactifs.
        Les graphiques incluent deux histogrammes, une carte choropleth mondiale et une carte choropleth pour les équipes.

    Interactivité :
        Utilisation de Dash pour créer une application web interactive.
        Mise en place de plusieurs callbacks pour mettre à jour les graphiques en fonction des sélections de l'utilisateur.
	
	Lancement de l'Application :
		L'application est lancée avec app.run(debug=True).
	
### Modification ou Extension du Code

Si vous souhaitez modifier ou étendre le code, suivez ces étapes :

1. Consultez la partie Developper Guide pour comprendre l'architecture.
2. Modifiez les fichiers pertinents selon vos besoins.
3. Assurez-vous de mettre à jour la documentation au besoin.
4. Soumettez une demande d'extraction (pull request) avec vos modifications.

## Requirements.txt

Le fichier `requirements.txt` contient la liste des packages nécessaires. Installez-les en utilisant la commande :

```bash
pip install -r requirements.txt
