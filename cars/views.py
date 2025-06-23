from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render, get_object_or_404

from .models import Cars, Category, TagPost

menu = [
    {'title': 'About page', 'url_name': 'about'},
    {'title': 'Add article', 'url_name': 'add_model'},
    {'title': 'Feedback', 'url_name': 'contact'},
    {'title': 'Log In', 'url_name': 'login'},
]


def index(request):
    posts = Cars.published.all()
    data = {
        'title': 'HomePage',
        'menu': menu,
        'cars': posts,
        'country_selected': 0,
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
        'country_selected': 1,
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


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Cars.published.filter(cat_id=category.pk)
    data = {
        'title': f'Country: {category.name}',
        'menu': menu,
        'cars': posts,
        'country_selected': category.pk,
    }
    return render(request, 'cars/index.html', context=data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Cars.Status.PUBLISHED)

    data = {
        'title': f'Tag: {tag.tag}',
        'menu': menu,
        'cars': posts,
        'country_selected': None,
    }

    return render(request, 'cars/index.html', context=data)
