from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Cars.Status.PUBLISHED)


class Cars(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0,
        PUBLISHED = 1,

    name = models.CharField(max_length=255, verbose_name='Model')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    year = models.IntegerField(validators=[MaxValueValidator(2026)])
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = (models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                        default=Status.DRAFT))
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')
    vin = models.OneToOneField('VinNumber', on_delete=models.PROTECT, null=True, blank=True, related_name='car')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'The most cheep cars '
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Country')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class VinNumber(models.Model):
    number = models.CharField(max_length=17, unique=True)

    def __str__(self):
        return self.number
