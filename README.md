# Intro
Ce projet est le premier ensemble d'étapes à suivre dans le cadre de la formation "Apprendre à programmer en Python : Confirmé", pour créer et configuer un projet en Django et Django Rest Framework.

# Environnement et création du projet
## Créer le répertoire du projet
```
$ mkdir mpa_exa
$ cd mpa_exa
```

## Créer un environnement virtuel
Cet environnement est utilisé pour isoler notre projet et gérer les librairies installées indépendamment d'autres projets locaux
```
$ python3 -m venv env
$ source env/bin/activate
```
On Windows use 
```
$ env\Scripts\activate
```

## Installer Django et Django REST framework
```
$ pip install django
$ pip install djangorestframework
```

## Créer une application Django
```
$ django-admin startproject mpa_exa .
$ django-admin startapp account
```