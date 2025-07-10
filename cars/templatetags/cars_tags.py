from django import template
from django.db.models import Count

import cars.views as views
from cars.models import Category, TagPost
from cars.utils import menu

register = template.Library()


@register.simple_tag
def get_menu():
    return menu


@register.inclusion_tag('cars/list_models.html')
def show_countries(country_selected=0):
    countries = Category.objects.annotate(total=Count('posts')).filter(total__gt=0)
    return {'countries': countries, 'country_selected': country_selected}


@register.inclusion_tag('cars/list_tags.html')
def show_all_tags(country_selected=0):
    return {'tags': TagPost.objects.annotate(total=Count('tags')).filter(total__gt=0)}
