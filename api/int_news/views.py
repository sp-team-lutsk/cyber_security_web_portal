from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import  GenericAPIView, ListCreateAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAdminUser
from .serializers import News_int_Serializer
from .models import News_int


class Post_int(ListCreateAPIView):
    queryset = News_int.objects.all()
    serializer_class = News_int_Serializer

class PostUpd_int(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = News_int.objects.all()
    serializer_class = News_int_Serializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)