from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render, get_object_or_404

from .models import Cars

menu = [
    {'title': 'About page', 'url_name': 'about'},
    {'title': 'Add article', 'url_name': 'add_model'},
    {'title': 'Feedback', 'url_name': 'contact'},
    {'title': 'Log In', 'url_name': 'login'},
]

data_db = [
    {'id': 1, 'title': 'Toyota',
     'content': '''Выпускается с 1982 года  по настоящее время.
     Сборка осуществляется в Японии, США, Австралии (до 2017 года), России (до 2022 года) и Китае.Тип кузова — 4‑дверный седан (5‑местный). 
     Компоновка — FWD, AWD (для США). Двигатель — ДВС, гибрид. Трансмиссия — АКПП, МКПП.'''},
    {'id': 2, 'title': 'Mazda', 'content': 2010},
    {'id': 3, 'title': 'Nissan', 'content': 2008},
]

models_db = [
    {'id': 1, 'model': 'Toyota'},
    {'id': 2, 'model': 'Mazda'},
    {'id': 3, 'model': 'Nissan'},
]


def index(request):
    posts = Cars.objects.filter(is_published=1)
    data = {
        'title': 'HomePage',
        'menu': menu,
        'cars': posts,
        'mod_selected': 0,
    }
    return render(request, 'cars/index.html', context=data)


def about(request):
    return render(request, 'cars/about.html', {'title': 'About page', 'menu': menu})


def show_post(request, post_slug):
    post = get_object_or_404(Cars, slug=post_slug)

    data = {
        'name': post.name,
        'menu': menu,
        'post': post,
        'mod_selected': 1,
    }

    return render(request, 'cars/post.html', data)


def add_model(request):
    return HttpResponse('Add model')


def contact(request):
    return HttpResponse('Feedback')


def login(request):
    return HttpResponse('Log In')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def show_model(request, model_id):
    data = {
        'title': 'View Model',
        'menu': menu,
        'cars': data_db,
        'mod_selected': model_id,
    }
    return render(request, 'cars/index.html', context=data)
