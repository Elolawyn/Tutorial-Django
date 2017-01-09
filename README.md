# Tutorial-Django
Tutorial sobre Django

<div id='index'/>
## Índice

1. [Entorno](#seccion01)
2. [Instalación](#seccion02)
3. [Parte 1: Introducción](#seccion1)
4. [Parte 2: Base de Datos y Administración](#seccion2)
5. [Parte 3: Vistas](#seccion3)

<div id='seccion01'/>
## Entorno

[Volver al índice](#index)

1. Python 3.5.2
2. Django 1.10.5
3. Ubuntu 16.04.1 LTS
4. SQLite

<div id='seccion02'/>
## Instalación

[Volver al índice](#index)

```bash
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install -y python3
sudo apt-get install -y python3-pip
python3 -V
pip3 -V
sudo pip3 install django
python3 -m django --version
```

<div id='seccion1'/>
## Parte 1: Introducción

[Volver al índice](#index)

### Crear proyecto

Todos los comandos que impliquen a **manage.py** se deben ejecutar en el directorio en el que esté. En el ejemplo, **nombreproyecto** es **tutorial**
```bash
django-admin startproject <nombreproyecto>
cd <nombreproyecto>
python3 manage.py runserver
```
Se puede comprobar que el servidor funciona accediendo a [http://localhost:8000](http://localhost:8000) en el navegador.

### Crear app

1. Una app es una aplicación web que hace algo.
2. Un proyecto es un conjunto de configuraciones y apps de un sitio web. En el ejemplo, **nombreapp** es **polls**

```bash
python3 manage.py startapp <nombreapp>
```

### Primera vista

Abrir fichero **polls/views.py** y añadir:

```python
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hola mundo. Estás en la página index de la app polls")
```

Abrir fichero **polls/urls.py** y añadir:

```python
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'), # Ruta de página de index
]
```

Abrir fichero **tutorial/urls.py** y añadir:

```python
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^polls/', include('polls.urls')), # Incluir las rutas de la app polls a partir de sitio.com/polls/
    url(r'^admin/', admin.site.urls),
]
```

<div id='seccion2'/>
## Parte 2: Base de Datos y Administración

[Volver al índice](#index)

### Ajustes

Abrir el fichero **tutorial/settings.py** y configurar la base de datos, la zona horaria y el idioma. En el tutorial se usará **SQLite**. Después ejecutamos el siguiente comando para crear las bases de datos para las aplicaciones indicadas en el fichero anterior.

```bash
python3 manage.py migrate
```

### Modelo

Abrir fichero **polls/models.py** y añadir:

```python
import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
```

Abrir el fichero **tutorial/settings.py** y añadir nuestra app a la lista:

```python
INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Convertimos los cambios hechos al modelo en una migración ejecutando el siguiente comando. En el ejemplo, **nombremigracion** es **polls**

```bash
python3 manage.py makemigrations <nombremigracion>
```

Comprobar cómo se van a realizar los cambios a la base de datos o si hay algún problema con los comandos:

```bash
python3 manage.py sqlmigrate <nombremigracion> 0001
python3 manage.py check
```

Aplicamos la migración a la base de datos:

```bash
python3 manage.py migrate
```

Resumen:

```bash
Cambiar modelo
python3 manage.py makemigrations <nombremigracion>
python3 manage.py migrate
```

### API de base de datos

```python
# Consultas
Question.objects.all()
Question.objects.filter(id=1) # Si no existe, lanzar excepción DoesNotExist
Question.objects.filter(question_text__startswith='¿Qué')
Question.objects.get(pub_date__year=timezone.now().year)
Question.objects.get(pk=1) # pk = primary key
q.choice_set.all() # Acceso a las respuestas de la pregunta
q.choice_set.count()
Choice.objects.filter(question__pub_date__year=timezone.now().year) # La API es capaz de seguir relaciones

# Crear 
q = Question(question_text="¿Qué pasa?", pub_date=timezone.now())
q.choice_set.create(choice_text='No mucho', votes=0)
q.save()

# Acceso atributos y métodos
q.id
q.question_text
q.was_published_recently()

# Actualización
q.question_text = "¿Qué hora es?"
q.save()

# Borrado
q.delete()
```

### Administración

Ejecutar:

```bash
python3 manage.py createsuperuser
Username: admin
Email address: admin@example.com
Password: **********
Password (again): *********
```

Lanzar el servidor y acceder a [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) en el navegador. Abrir el fichero **polls/admin.py** y añadir:

```python
from django.contrib import admin

from .models import Question

admin.site.register(Question)
```

Ahora se pueden añadir preguntas desde el administrador.

<div id='seccion3'/>
## Parte 3: Vistas

[Volver al índice](#index)

### Subparte 1

Hacer

