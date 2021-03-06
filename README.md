# Tutorial-Django
Tutorial sobre Django

<div id='index'/>
## Índice

1. [Entorno](#seccion01)
2. [Instalación](#seccion02)
3. [Parte 1: Introducción](#seccion1)
4. [Parte 2: Base de Datos y Administración](#seccion2)
5. [Parte 3: Vistas](#seccion3)
6. [Parte 4: Formularios](#seccion4)
7. [Parte 5: Testeando la aplicación](#seccion5)
8. [Parte 6: Aspecto](#seccion6)

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

Crear directorio **templates** dentro de **polls**. Crear dentro del nuevo directorio **templates** un direrctorio llamado **polls**. Crear el fichero **index.html** dentro y añadir:

```HTML+Django
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No hay consultas.</p>
{% endif %}
```

Crear el fichero **polls/templates/polls/detail.html** y añadir:

```HTML+Django
<h1>{{ question.question_text }}</h1>
<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }}</li>
{% endfor %}
</ul>

```

Abrir fichero **polls/views.py** y añadir:

```python
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "Resultados de la pregunta %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("Formulario para votar por la pregunta %s." % question_id)
```

Abrir fichero **polls/urls.py** y añadir:

```python
from django.conf.urls import url

from . import views

app_name = 'polls' # Namespace

urlpatterns = [
    # /polls/
    url(r'^$', views.index, name='index'),
    # /polls/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # /polls/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
```

<div id='seccion4'/>
## Parte 4: Formularios

[Volver al índice](#index)

### Añadir formularios

Abrir el fichero **polls/templates/polls/detail.html** y añadir:

```HTML+Django
<h1>{{ question.question_text }}</h1>

{% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}

<form action="{% url 'polls:vote' question.id %}" method="post">
{% csrf_token %}
{% for choice in question.choice_set.all %}
    <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}" />
    <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br />
{% endfor %}
<input type="submit" value="Votar" />
</form>

```

Crear el fichero **polls/templates/polls/results.html** y añadir:

```HTML+Django
<h1>{{ question.question_text }}</h1>

<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
{% endfor %}
</ul>

<a href="{% url 'polls:detail' question.id %}">¿Quiere votar de nuevo?</a>

```

Abrir fichero **polls/views.py** y añadir:

```python
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Choice, Question
# ...
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
    
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
```

### Uso de vistas genéricas

Abrir fichero **polls/urls.py** y añadir:

```python
from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
```

Abrir fichero **polls/views.py** y añadir:

```python
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
```

<div id='seccion5'/>
## Parte 5: Testeando la aplicación

[Volver al índice](#index)

### Introducción

Hay un bug en la aplicación que vamos a corregir. El método **Question.was_published_recently()** devuelve true si la noticia es futura. Para comprobar el código, escribimos el test en el fichero **polls/tests.py**:

```python
import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Question

class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
```

Ejecutamos el test:

```bash
python3 manage.py test polls
```

Corregimos el error en el fichero **polls/models.py**:

```python
def was_published_recently(self):
    now = timezone.now()
    return now - datetime.timedelta(days=1) <= self.pub_date <= now
```

Ahora el test debería dar positivo. Vamos a agregar nuevas comprobaciones al fichero **polls/tests.py**:

```python
def test_was_published_recently_with_old_question(self):
    """
    was_published_recently() should return False for questions whose
    pub_date is older than 1 day.
    """
    time = timezone.now() - datetime.timedelta(days=30)
    old_question = Question(pub_date=time)
    self.assertIs(old_question.was_published_recently(), False)

def test_was_published_recently_with_recent_question(self):
    """
    was_published_recently() should return True for questions whose
    pub_date is within the last day.
    """
    time = timezone.now() - datetime.timedelta(hours=1)
    recent_question = Question(pub_date=time)
    self.assertIs(recent_question.was_published_recently(), True)
```

### Testeando vistas

La vista index muestra preguntas con fecha futura, vamos a solucionarlo. Modificamos el fichero **polls/views.py**:

```python
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
```

Añadir nuevos tests para probar la vista al fichero **polls/tests.py**:

```python
from django.urls import reverse

def create_question(question_text, days):
    """
    Creates a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay consultas.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        """
        Questions with a pub_date in the past should be displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_a_future_question(self):
        """
        Questions with a pub_date in the future should not be displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No hay consultas.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        should be displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
```

También hay que evitar el acceso a los detalles de una pregunta futura. Modificamos el fichero **polls/views.py**:

```python
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
```

Añadir nuevos tests para probar la vista al fichero **polls/tests.py**:

```python
class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        """
        The detail view of a question with a pub_date in the future should
        return a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        """
        The detail view of a question with a pub_date in the past should
        display the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
```

<div id='seccion6'/>
## Parte 6: Aspecto

[Volver al índice](#index)

### Por hacer

Por hacer
