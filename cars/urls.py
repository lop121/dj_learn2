from django.urls import path, re_path, register_converter

from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.CarsHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('add_new_car/', views.AddCar.as_view(), name='add_car'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('category/<slug:cat_slug>/', views.CarsCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
]
