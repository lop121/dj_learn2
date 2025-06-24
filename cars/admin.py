from itertools import count

from django.contrib import admin, messages

from cars.models import Cars, Category


@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    fields = ['name', 'slug', 'year', 'cat', 'tags']
    exclude = ['is_published']
    # readonly_fields = ['slug']
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'time_create', 'is_published', 'brief_info')
    list_display_links = ('name',)
    ordering = ['time_create', 'name']
    list_editable = ('is_published',)
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['name__startswith', 'cat__name']
    list_filter = ['cat__name', 'is_published']

    @admin.display(description='The novelty of the car', ordering='year')
    def brief_info(self, cars: Cars):
        if cars.year > 2015:
            return f'New car ({cars.year})'
        elif cars.year >= 2000:
            return f'Recent ({cars.year})'
        else:
            return f'Rare ({cars.year})'

    @admin.action(description='Published selected models')
    def set_published(self, request, queryset):
        counts = queryset.update(is_published=Cars.Status.PUBLISHED)
        self.message_user(request, f"Edited {counts} models")

    @admin.action(description='Unpublished selected models')
    def set_draft(self, request, queryset):
        counts = queryset.update(is_published=Cars.Status.DRAFT)
        self.message_user(request, f"Unpublished {counts} models", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
