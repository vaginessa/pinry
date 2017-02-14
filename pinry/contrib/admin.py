from django.contrib import admin

from .models import ImagePin



@admin.register(ImagePin)
class PinAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'get_tags_as_string', 'user']
    filter_horizontal = ['tags']

