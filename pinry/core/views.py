from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.template.response import TemplateResponse

from rest_framework import viewsets, permissions

from .models import Tag, Pin
from .serializers import UserSerializer, TagSerializer, PinSerializer
from .permissions import IsUserOrReadOnly, IsAdminOrReadOnly


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


def login_view(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('core:recent-pins')
        else:
            messages.add_message(request, messages.WARN, 'Your username or password was incorrect.')
    return TemplateResponse(request, 'users/login.html')

