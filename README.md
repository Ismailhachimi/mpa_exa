# Intro
Ce projet est le premier ensemble d'étapes à suivre dans le cadre de la formation "Apprendre à programmer en Python : Confirmé", pour créer et configuer un projet en Django et Django Rest Framework.

# Environnement et création du projet
## Créer le répertoire du projet
```shell
$ mkdir mpa_exa
$ cd mpa_exa
```

## Créer un environnement virtuel
Cet environnement est utilisé pour isoler notre projet et gérer les librairies installées indépendamment d'autres projets locaux
```shell
$ python3 -m venv env
$ source env/bin/activate
```
On Windows use 
```powershell
$ env\Scripts\activate
```

## Installer Django et Django REST framework
```shell
$ pip install django
$ pip install djangorestframework
```

## Créer une application Django
```shell
$ django-admin startproject mpa_exa .
$ django-admin startapp account
```

## Ligne de commande Django Shell
```shell
$ python manage.py shell
```
À travers cette commande, nous pouvons intéragir avec les objets dans la base de données avec les opérations de recherche, création, mise à jour et suppression.

Exemple d'opérations appliquées à l'objet User d'utilisateur natif de Django.

```python
>>> from django.contrib.auth.models import User
>>> 
>>> # récupérer tous les objets dans la base
>>> User.objects.all()  
>>> 
>>> # récupérer une liste contenant l'utilisateur admin
>>> User.objects.filter(email="admin@mpaexa.fr")  
>>>
>>> # récupérer le premier utilisateur avec un mail '.fr'
>>> admin_user = User.objects.filter(email__contains=".fr").first()
>>> 
>>> # mettre à jour tous les utilisateurs avec un mail français
>>> admin_user.
>>> # récupérer tous les utilisateurs avec un mail français
>>> User.objects.filter(email__contains=".fr")  
```

# Premières étapes
## Créer un premier modèle
Créer un nouveau manager d'utilisateur, ce qui est la classe qui permet à Django de gérer le modèle.

Ce manager est une classe dans un fichier `account/managers.py` que nous allons utiliser dans le champ `object` dans la classe `User` à créer.

Ajouter le modèle en créant la classe User :
```python
class User(AbstractUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    object = UserManager()
    ...
    email = models.EmailField(...)
    ...
```

Pour que Django fasse référence à notre nouveau modèle `User` comme son modèle d'utilisateur natif,
il faut ajouter la ligne suivante dans `settings.py` : 
```python
AUTH_USER_MODEL = 'account.User'
```

Enregistrer le modèle dans l'administration pour qu'un administrateur puisse le trouver.
```python
class UserAdmin(admin.ModelAdmin):
    ... 

admin.site.register(User, UserAdmin)
```

Finalement, pour que les modifications soient prises en considération au niveau de la base, préparer et puis appliquer la migration :

```shell
$ python manage.py makemigrations account
$ python manage.py migrate
```

Nous nous rendons compte d'un problème ... migration d'un objet qui est déjà migré mais de différente référence. Comment faire ?

En générale, il faut éviter de modifier les objets natifs après première migrations, parce que leur modification doit être prévue dès le début.

Reprennant d'une version propre et néttoyer la base. Le plus simple est de supprimer le fichier `db.sqlite3`. Dans le cas d'une base MySQL ou PostgreSQL, il faudra passer par la ligne de commande `shell` ou `dbshell` pour le faire en SQL et suivre les instructions d'erreurs après la commande de migration.

```shell
$ python manage.py dbshell
```

## Le nouveau utilisateur dans le `shell`
Afin d'utiliser le nouveau modèle d'utilisateur, nous avons l'importer directement de `account.models`:
```python
>>> from account.models import User
>>> User.objects.all()
>>> 
>>> # créer un superadmin
>>> User.objects.create_superuser(
        email="***@***.**", 
        password="********"
    ).save()
```

# API de l'application `account`
Dans cette section, nous allons créer le répértoire `api` pour :
* `serializers.py` : 
    
    Les sérialiseurs fonctionnent de manière très similaire aux classes Form et ModelForm de Django.
    
    Ils permettent de convertir des données complexes telles que des querysets et des instances de modèle, en types de données Python natifs

* `views.py` : 

    Les `ViewSets` permettent d'avoir la logique d'un groupe de vues dans la même classe.

* `permissions.py` : 

    Les permissions regroupent la logique d'authentification et d'autorisation sous forme de classes réutilisables pour vérifier et valider l'identité et les droits.

##  Plus de détails ? 
Voir le code 

# Conteneuriser son application
Un Dockerfile est un fichier texte qui contient des instructions sur la façon dont l'image Docker sera construite. Un Dockerfile contient les directives ci-dessous.

* **FROM** : la directive définit l'image de base à partir de laquelle le conteneur Docker sera construit.
* **WORKDIR** : la directive définit le répertoire de travail dans l'image créée.
* **RUN** : la directive exécute les commandes dans le conteneur.
* **COPY** : la directive copie les fichiers du système de fichiers dans le conteneur.
* **CMD** : la directive définit les commandes exécutables dans le conteneur.

## Construction de l'image Docker

Pour construire l'image Docker à partir du Dockerfile que nous avons créé :
```shell
$ docker build --tag mpa_exa:latest .
```

Pour afficher les images Docker disponible sur notre machine :
```shell
$ docker image ls
```

## Création et exécution du conteneur Docker

Pour construire et exécuter un conteneur Docker à partir de l'image Docker que nous avons créée :
```shell
$ docker run --name mpa_exa -d -p 8000:8000 mpa_exa:latest
```

Pour lister tous les conteneurs Docker en cours d'exécution :
```shell
$ docker container ps
```

## Arrêt de conteneur et suppression de ce dernier et l'image

Pour arrêter un conteneur :
```shell
$ docker stop <container-id>
```

Pour supprimer un conteneur
```shell
$ docker rm <container-id>
```

Pour supprimer une image
```shell
$ docker rmi <image-id>
```

À noter que dans notre cas, le docker est disponible depuis `0.0.0.0:8000`.

# Notes
You can use `example_local.py` as a local settings file by renaming it to `local.py`.

`prod.py` can be used by renaming it to `local.py` in a deployment pipeline. Make sure to have a pre-prod environment to test it (locally on in that environment).