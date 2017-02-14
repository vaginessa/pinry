from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.edit import CreateView

from rest_framework import viewsets, permissions

from .models import Tag, Pin
from .serializers import UserSerializer, TagSerializer, PinSerializer
from .permissions import IsUserOrReadOnly, IsAdminOrReadOnly
from .forms import PinForm


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
        return queryset.select_subclasses()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PinFormView(CreateView):
    template_name = 'core/pin_form.html'
    form_class = PinForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.add_message(self.request, messages.INFO, 'Successfully added new pin.')
        return super(PinFormView, self).form_valid(form)

