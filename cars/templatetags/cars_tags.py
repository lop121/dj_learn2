from django import template
import cars.views as views
from cars.models import Category

register = template.Library()


@register.inclusion_tag('cars/list_models.html')
def show_countries(country_selected=0):
    countries = Category.objects.all()
    return {'countries': countries, 'country_selected': country_selected}
