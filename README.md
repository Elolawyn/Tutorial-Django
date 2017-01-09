# Tutorial-Django
Tutorial sobre Django

<div id='index'/>
## Índice

1. [Requisitos](#seccion01)
2. [Instalación](#seccion02)
3. [Parte 1: Introducción](#seccion1)
4. [Parte 2: Base de Datos y Administración](#seccion2)

<div id='seccion01'/>
## Requisitos

[Volver al índice](#index)

1. Python 3.5.2
2. Django 1.10.5

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
2. Un proyecto es un conjunto de configuraciones y apps de un sitio web.En el ejemplo, **nombreapp** es **polls**

```bash
python manage.py startapp <nombreapp>
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

Por hacer
