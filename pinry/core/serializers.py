from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Tag
from .models import Pin


class TagSerializer(serializers.HyperlinkedModelSerializer):
    api_url = serializers.HyperlinkedIdentityField(view_name='core:api:tag-detail')

    class Meta:
        model = Tag
        fields = ['api_url', 'id', 'title', 'slug']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    api_url = serializers.HyperlinkedIdentityField(view_name='core:api:user-detail')

    class Meta:
        model = User
        fields = ['api_url', 'id', 'username']


class PinSerializer(serializers.HyperlinkedModelSerializer):
    api_url = serializers.HyperlinkedIdentityField(view_name='core:api:pin-detail')
    user = UserSerializer(read_only=True)
    tags = TagSerializer(many=True)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        pin = Pin.objects.create(**validated_data)
        for tag in tags:
            pin.add_tag(tag['title'])
        return pin

    class Meta:
        model = Pin
        fields = ['api_url', 'id', 'title', 'url', 'get_url_domain', 'tags', 'user', 'get_image', 'get_thumbnail']

