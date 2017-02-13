from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import permissions

from .models import Tag
from .models import Pin
from .serializers import UserSerializer
from .serializers import TagSerializer
from .serializers import PinSerializer
from .permissions import IsUserOrReadOnly
from .permissions import IsAdminOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by('-id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
            IsAdminOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by('-id')
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
            IsAdminOrReadOnly]


class PinViewSet(viewsets.ModelViewSet):
    queryset = Pin.objects.order_by('-id')
    serializer_class = PinSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
            IsUserOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        userid = self.request.query_params.get('userid', None)
        if userid is not None:
            queryset = queryset.filter(user__id=userid)
        tagid = self.request.query_params.get('tagid', None)
        if tagid is not None:
            queryset = queryset.filter(tags__id=tagid)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

