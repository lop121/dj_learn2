from django.core.validators import MaxValueValidator
from django.db import models


class Cars(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField(validators=[MaxValueValidator(2026)])
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.name
