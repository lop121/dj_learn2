from django import forms

from cars.models import Category, TagPost, VinNumber


class AddCarForm(forms.Form):
    name = forms.CharField(max_length=100, label='Name car')
    slug = forms.SlugField(max_length=255, label='URL')
    year = forms.IntegerField(max_value=2026, min_value=1000, label='Year')
    is_published = forms.BooleanField(required=False, initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Country', empty_label='Country not selected')
    vin = forms.ModelChoiceField(queryset=VinNumber.objects.all(), label='Vin Number', required=False)
