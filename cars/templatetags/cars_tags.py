from django import template
import cars.views as views

register = template.Library()


@register.simple_tag(name='getmodel')
def get_models():
    return views.models_db


@register.inclusion_tag('cars/list_models.html')
def show_models(model_selected=0):
    models = views.models_db
    return {'modeli': models, 'model_selected': model_selected}
