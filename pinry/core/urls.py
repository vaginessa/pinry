from django.conf.urls import url, include
from django.views.generic import TemplateView

from rest_framework import routers

from .views import UserViewSet
from .views import TagViewSet
from .views import PinViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tags', TagViewSet)
router.register(r'pins', PinViewSet)


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='core/pins.html'), name='recent-pins'),

    url(r'^$', TemplateView.as_view(template_name='core/pins.html'), name='login'),
    url(r'^$', TemplateView.as_view(template_name='core/pins.html'), name='logout'),
    url(r'^$', TemplateView.as_view(template_name='core/pins.html'), name='register'),

    url(r'^api/', include(router.urls, namespace='api')),
]

