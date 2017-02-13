from django.contrib import admin

from .models import Tag
from .models import Pin


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'get_number_of_pins']


@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'get_tags_as_string', 'user']
    filter_horizontal = ['tags']

