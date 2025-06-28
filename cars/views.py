from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView
from unicodedata import category

from .forms import AddCarForm, UploadFileForm
from .models import Cars, Category, TagPost, VinNumber, UploadFiles

menu = [
    {'title': 'About page', 'url_name': 'about'},
    {'title': 'Add a new car', 'url_name': 'add_car'},
    {'title': 'Feedback', 'url_name': 'contact'},
    {'title': 'Log In', 'url_name': 'login'},
]


# def index(request):
#     posts = Cars.published.all().select_related('cat')
#     data = {
#         'title': 'HomePage',
#         'menu': menu,
#         'cars': posts,
#         'country_selected': 0,
#     }
#     return render(request, 'cars/index.html', context=data)


class CarsHome(ListView):
    # model = Cars
    template_name = 'cars/index.html'
    context_object_name = 'cars'

    extra_context = {
        'title': 'HomePage',
        'menu': menu,
        'country_selected': 0,
    }

    def get_queryset(self):
        return Cars.published.all().select_related('cat')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'HomePage'
    #     context['menu'] = menu
    #     context['cars'] = Cars.published.all().select_related('cat')
    #     context['country_selected'] = int(self.request.GET.get('cat_id', 0))
    #     return context


def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'cars/about.html', {'title': 'About page', 'menu': menu, 'form': form})


def show_post(request, post_slug):
    post = get_object_or_404(Cars, slug=post_slug)

    data = {
        'name': post.name,
        'menu': menu,
        'post': post,
        'country_selected': 1,
    }

    return render(request, 'cars/post.html', data)


# def add_car(request):
#     if request.method == 'POST':
#         form = AddCarForm(request.POST, request.FILES)
#         if form.is_valid():
#             # try:
#             #     Cars.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except Exception as e:
#             #     form.add_error(None, f'Error: {e}')
#             form.save()
#             return redirect('home')
#     else:
#         form = AddCarForm()
#     data = {
#         'menu': menu,
#         'title': 'Add new car',
#         'form': form
#     }
#     return render(request, 'cars/addcar.html', context=data)


class AddCar(View):
    def get(self, request):
        form = AddCarForm()
        data = {
            'menu': menu,
            'title': 'Add new car',
            'form': form
        }
        return render(request, 'cars/addcar.html', context=data)

    def post(self, request):
        if request.method == 'POST':
            form = AddCarForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('home')

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


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts = Cars.published.filter(cat_id=category.pk).select_related('cat')
#     data = {
#         'title': f'Country: {category.name}',
#         'menu': menu,
#         'cars': posts,
#         'country_selected': category.pk,
#     }
#     return render(request, 'cars/index.html', context=data)


class CarsCategory(ListView):
    template_name = 'cars/index.html'
    context_object_name = 'cars'
    allow_empty = False

    def get_queryset(self):
        return Cars.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['cars'][0].cat
        context['title'] = 'Country - ' + cat.name
        context['menu'] = menu
        context['country_selected'] = cat.pk
        return context


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
