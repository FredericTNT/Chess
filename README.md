# Chess

## Table des matières
1. [Informations générales](#Informations_générales)
2. [Technologies](#technologies)
3. [Installation](#installation)
4. [Exécution](#Exécution)
4. [Maintenabilité du code (PEP 8)](#Maintenabilité_du_code)
## Informations_générales
***
Application hors ligne de gestion d'un tournoi d'échecs 
+ Interface utilisateur en mode console
+ Sauvegarde des données de l'application dans une base json
## Technologies
***
Technologies utilisées dans ce projet :
* [Windows 10 Famille](https://docs.microsoft.com/fr-fr/windows/whats-new/whats-new-windows-10-version-21h1) : version 21H1 
* [Python](https://docs.python.org/fr/3.10/) : version 3.10.0
* [Library - tinydb](https://pypi.org/project/tinydb/) : version 4.5.2
* [Library - colored](https://pypi.org/project/colored/) : version 1.4.3
* [Library - flake8](https://pypi.org/project/flake8/) : version 4.0.1
* [Library - flake8-html](https://pypi.org/project/flake8-html/) : version 0.4.1
* [module - operator(attrgetter, itemgetter)](https://docs.python.org/fr/3/library/operator.html)
## Installation
***
Réaliser l'installation avec le terminal Windows PowerShell 

Le clonage (git clone) se fait dans un répertoire Chess et ses sous-répertoires models, views et controllers
```
$ git clone https://github.com/FredericTNT/Chess
$ cd Chess
$ python -m venv <nom environnement>
$ <nom environnement>/scripts/activate
$ pip install -r requirements.txt
```
## Exécution
***
L'application se lance en exécutant le programme main.py dans l'environnement virtuel activé
```
$ python main.py
```

La base json de l'application dénommée chess_db.json est créée dans le répertoire Chess lors de la première exécution.
## Maintenabilité_du_code
A compléter
<!---
## FAQs
***
A list of frequently asked questions
1. **This is a question in bold**
Answer of the first question with _italic words_. 
2. __Second question in bold__ 
To answer this question we use an unordered list:
* First point
* Second Point
* Third point
3. **Third question in bold**
Answer of the third question with *italic words*.
4. **Fourth question in bold**
| Headline 1 in the tablehead | Headline 2 in the tablehead | Headline 3 in the tablehead |
|:--------------|:-------------:|--------------:|
| text-align left | text-align center | text-align right |
-->