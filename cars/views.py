from django.http import HttpResponse


def index(request):
    return HttpResponse("Страница приложения cars.")


def brand(request, brand_id):
    return HttpResponse(f'<h1>Марки машин<h1/> <p> id: {brand_id}</p>')


def brand_by_slug(request, brand_slug):
    return HttpResponse(f'<h1>Марки машин<h1/> <p>Название: {brand_slug}</p>')


def archive(request, year):
    return HttpResponse(f'<h1>Архив машин<h1/> <p>Год: {year}</p>')
