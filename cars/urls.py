from django.urls import path, re_path, register_converter

from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('add_model/', views.add_model, name='add_model'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('model/<int:model_id>/', views.show_model, name='model'),

]
