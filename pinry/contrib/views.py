from django.contrib import messages
from django.views.generic.edit import CreateView

from rest_framework import viewsets, permissions

from pinry.core.views import PinFormView

from .forms import ImagePinForm


class ImagePinFormView(PinFormView):
    template_name = 'contrib/image_pin_form.html'
    form_class = ImagePinForm

