from django.http import HttpResponse

def index(request):
    return HttpResponse("Hola mundo. Estás en la página index de la app polls")
