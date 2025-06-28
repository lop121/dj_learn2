from django import forms

from cars.models import Category, TagPost, VinNumber, Cars


class AddCarForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Country', empty_label='Country not selected')
    vin = forms.ModelChoiceField(queryset=VinNumber.objects.all(), label='Vin Number', required=False)

    class Meta:
        model = Cars
        fields = ['name', 'slug', 'year', 'photo', 'is_published', 'cat', 'tags', 'vin']
        labels = {'slug': 'URL'}


class UploadFileForm(forms.Form):
    file = forms.ImageField(label='File')
