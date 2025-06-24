from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render, get_object_or_404

from .forms import AddCarForm
from .models import Cars, Category, TagPost, VinNumber

menu = [
    {'title': 'About page', 'url_name': 'about'},
    {'title': 'Add a new car', 'url_name': 'add_car'},
    {'title': 'Feedback', 'url_name': 'contact'},
    {'title': 'Log In', 'url_name': 'login'},
]


def index(request):
    posts = Cars.published.all().select_related('cat')
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


def add_car(request):
    if request.method == 'POST':
        form = AddCarForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            try:
                Cars.objects.create(**form.cleaned_data)
                return redirect('home')
            except Exception as e:
                form.add_error(None, f'Error: {e}')
    else:
        form = AddCarForm()
    data = {
        'menu': menu,
        'title': 'Add new car',
        'form': form
    }
    return render(request, 'cars/addcar.html', context=data)


def contact(request):
    return HttpResponse('Feedback')


def login(request):
    return HttpResponse('Log In')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Cars.published.filter(cat_id=category.pk).select_related('cat')
    data = {
        'title': f'Country: {category.name}',
        'menu': menu,
        'cars': posts,
        'country_selected': category.pk,
    }
    return render(request, 'cars/index.html', context=data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Cars.Status.PUBLISHED).select_related('cat')

    data = {
        'title': f'Tag: {tag.tag}',
        'menu': menu,
        'cars': posts,
        'country_selected': None,
    }

    return render(request, 'cars/index.html', context=data)
