from audioop import reverse

from django.core.paginator import Paginator
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
from .utils import DataMixin


class CarsHome(DataMixin, ListView):
    template_name = 'cars/index.html'
    context_object_name = 'cars'
    title_page = 'HomePage'
    country_selected = 0

    def get_queryset(self):
        return Cars.published.all().select_related('cat')


def about(request):
    contact_list = Cars.published.all()
    paginator = Paginator(contact_list, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cars/about.html', {'title': 'About page', 'page_obj': page_obj})


class ShowPost(DataMixin, DetailView):
    template_name = 'cars/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].name)

    def get_object(self, queryset=None):
        return get_object_or_404(Cars.published, slug=self.kwargs[self.slug_url_kwarg])


class AddCar(DataMixin, CreateView):
    form_class = AddCarForm
    template_name = 'cars/addcar.html'
    title_page = 'Add a new car'


class UpdateCar(DataMixin, UpdateView):
    model = Cars
    fields = ['name', 'year', 'photo', 'is_published', 'cat']
    template_name = 'cars/addcar.html'
    success_url = reverse_lazy('home')
    title_page = 'Edit post'


class DeleteCar(DataMixin, DeleteView):
    model = Cars
    template_name = 'cars/car_confirm_delete.html'
    context_object_name = 'car'
    success_url = reverse_lazy('home')
    title_page = 'Delete car'


def contact(request):
    return HttpResponse('Feedback')


def login(request):
    return HttpResponse('Log In')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class CarsCategory(DataMixin, ListView):
    template_name = 'cars/index.html'
    context_object_name = 'cars'
    allow_empty = False

    def get_queryset(self):
        return Cars.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['cars'][0].cat
        return self.get_mixin_context(context, title='Country - ' + cat.name,
                                      country_selected=cat.pk,
                                      )


class TagPostList(DataMixin, ListView):
    template_name = 'cars/index.html'
    context_object_name = 'cars'
    allow_empty = False

    def get_queryset(self):
        return Cars.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context,
                                      title='Tag: ' + tag.tag,
                                      )
