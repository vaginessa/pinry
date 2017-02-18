from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^contrib/', include('pinry.contrib.urls', namespace='contrib')),
    url(r'^', include('pinry.core.urls', namespace='core')),
]

