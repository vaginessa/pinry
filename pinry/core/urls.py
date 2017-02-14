from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.contrib.auth.views import login, logout

from rest_framework import routers

from .views import UserViewSet, TagViewSet, PinViewSet, PinFormView


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tags', TagViewSet)
router.register(r'pins', PinViewSet)


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='core/pins.html'), name='recent-pins'),

    url(r'^new-pin/$', PinFormView.as_view(), name='pin-form'),

    url(r'^login/$', login, {'template_name': 'users/login.html'}, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^$', TemplateView.as_view(template_name='core/pins.html'), name='register'),

    url(r'^api/', include(router.urls, namespace='api')),
]

