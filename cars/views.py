from audioop import reverse

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from dns.update import Update
from unicodedata import category
from wheel.cli import tags_f

from .forms import AddCarForm, UploadFileForm
from .models import Cars, Category, TagPost, VinNumber, UploadFiles

menu = [
    {'title': 'About page', 'url_name': 'about'},
    {'title': 'Add a new car', 'url_name': 'add_car'},
    {'title': 'Feedback', 'url_name': 'contact'},
    {'title': 'Log In', 'url_name': 'login'},
]


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


def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'cars/about.html', {'title': 'About page', 'menu': menu, 'form': form})


class ShowPost(DetailView):
    model = Cars
    template_name = 'cars/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].name
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Cars.published, slug=self.kwargs[self.slug_url_kwarg])


class AddCar(CreateView):
    form_class = AddCarForm
    template_name = 'cars/addcar.html'
    # success_url = reverse_lazy('home')

    extra_context = {
        'menu': menu,
        'title': 'Add a new car',
    }


class UpdateCar(UpdateView):
    model = Cars
    fields = ['name', 'year', 'photo', 'is_published', 'cat']
    template_name = 'cars/addcar.html'
    success_url = reverse_lazy('home')

    extra_context = {
        'menu': menu,
        'title': 'Edit car',
    }


class DeleteCar(DeleteView):
    model = Cars
    template_name = 'cars/car_confirm_delete.html'
    context_object_name = 'car'
    success_url = reverse_lazy('home')

    extra_context = {
        'menu': menu,
        'title': 'Delete car',
    }


# class AddCar(View):
#     def get(self, request):
#         form = AddCarForm()
#         data = {
#             'menu': menu,
#             'title': 'Add new car',
#             'form': form
#         }
#         return render(request, 'cars/addcar.html', context=data)
#
#     def post(self, request):
#         if request.method == 'POST':
#             form = AddCarForm(request.POST, request.FILES)
#             if form.is_valid():
#                 form.save()
#                 return redirect('home')
#
#         data = {
#             'menu': menu,
#             'title': 'Add new car',
#             'form': form
#         }
#         return render(request, 'cars/addcar.html', context=data)


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


class TagPostList(ListView):
    template_name = 'cars/index.html'
    context_object_name = 'cars'
    allow_empty = False

    def get_queryset(self):
        return Cars.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = 'Tag: ' + tag.tag
        context['menu'] = menu
        context['country_selected'] = None
        return context
