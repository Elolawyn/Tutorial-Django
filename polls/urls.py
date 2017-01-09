from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'), # Ruta de página de index
]
