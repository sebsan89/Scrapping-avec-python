# Projet 2 : Scrapping avec Python

Création d'un scrypt avec Python pour récupérer les données du site http://books.toscrape.com/.
Le depot est organisé en plusieurs branches:
    - Récupération des données d'un seul livre
    - Récupération des données de tout les livres d'une catégorie
    - Récupération des données de tout les livre du site avec image

les données seront stocké dans des fichiers CSV, chaque fichier désignera une catégorie ``(catégorie.csv)`` 
Les images seront nommé suivant les numero UPC de chaque livre et seront organisé dans les dossier portant le nom de la catégorie rataché

## Pour commencer

Télécharger le fichier zip contenant le code ou effectuer un ``git clone``

### Pré-requis

Pour commencer, vous devez posséder les logiciel suivant

- Python 3.7 ou ulterieur
- PyPI
- venv  ``pip install venv``

### Installation

Les étapes d'installation....

Pour Windows :
   dans l'invite de commande : ``python -m venv env``  ``env/Scripts/activate``  ``pip install -r requirements.txt``   

Pour linux :
   dans le terminal : ``sudo py3 -m venv env``  ``source env/bin/activate``  ``pip3 install -r requirements.txt``   



## Démarrage
Pour Windows :
     ``python _fichierQueVousSouhaitez__.py``
	 
Pour Linux :
     ``py3 _fichierQueVousSouhaitez__.py``

## Fabriqué avec

Python 3

Librairies :
	beautifulsoup4==4.9.3
	requests==2.25.1
	lxml==4.6.2
	pylint==2.7.2
	
## Auteurs

Sebastien SANNAC, Projet organisé par OpenClassrooms sur le parcourt diplomant Python



