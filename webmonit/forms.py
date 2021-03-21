from django.forms import ModelForm

from .models import Page

class CreatePageForm(ModelForm):
    class Meta:
        model = Page
        fields = ['name', 'url', 'frequency']