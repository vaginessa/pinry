from django.conf.urls import url, include

from .views import ImagePinFormView


urlpatterns = [
    url(r'^new-image-pin/$', ImagePinFormView.as_view(), name='image-pin-form'),
]

