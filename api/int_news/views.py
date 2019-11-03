from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import  GenericAPIView, ListCreateAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAdminUser
from .serializers import NewsIntSerializer
from .models import NewsInt

class PostInt(ListCreateAPIView):
    queryset = NewsInt.objects.all()
    serializer_class = NewsIntSerializer

class PostUpdInt(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = NewsInt.objects.all()
    serializer_class = NewsIntSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)