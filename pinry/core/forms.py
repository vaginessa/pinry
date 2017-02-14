from django.forms import ModelForm

from .models import Pin


class PinForm(ModelForm):
    class Meta:
        model = Pin
        exclude = ['user',]

