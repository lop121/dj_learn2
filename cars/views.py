from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render
from django.template.context_processors import request
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string

menu = ['About page', 'Add article', 'Back contact', 'Log In']


class MyClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b


def index(request):
    # t = render_to_string('cars/index.html')
    # return HttpResponse(t)
    data = {
        'title': 'homePage',
        'menu': menu,
        'float': 7.10,
        'lst': [1, 2, 'abc', True],
        'set': {1, 2, 4, 5},
        'dict': {'key_1': 'value_1'},
        'obj': MyClass(1, 2),
        'tire': slugify('The Title Text')
    }
    return render(request, 'cars/index.html', context=data)


def about(request):
    return render(request, 'cars/about.html', {'title': 'About page'})


def brand(request, brand_id):
    return HttpResponse(f'<h1>Марки машин<h1/> <p> id: {brand_id}</p>')


def brand_by_slug(request, brand_slug):
    if request.POST:
        print(request.POST)
    return HttpResponse(f'<h1>Марки машин<h1/> <p>Название: {brand_slug}</p>')


def archive(request, year):
    if year > 2025:
        return redirect('home')
    return HttpResponse(f'<h1>Архив машин<h1/> <p>Год: {year}</p>')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
