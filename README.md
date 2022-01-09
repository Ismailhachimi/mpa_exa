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

