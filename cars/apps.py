from django.apps import AppConfig


class CarsConfig(AppConfig):
    verbose_name = 'My cars'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cars'
