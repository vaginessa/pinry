from django.forms import ModelForm

from pinry.core.forms import PinForm

from .models import ImagePin


class ImagePinForm(PinForm):
    class Meta:
        model = ImagePin
        exclude = ['user', 'image_width', 'image_height', 'thumbnail', 'thumbnail_width', 'thumbnail_height']

