from django.urls import path, re_path, register_converter

from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('brand/<int:brand_id>/', views.brand, name='brand'),
    path('brand/<slug:brand_slug>/', views.brand_by_slug, name='brand_slug'),
    path(r"archive/<year4:year>/", views.archive, name='archive')
]
