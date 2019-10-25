from django.contrib.auth import get_user_model  
from rest_framework import status
from rest_framework.generics import  GenericAPIView, ListCreateAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.views import APIView

from rest_framework.response import Response
from authentication.models import StdUser
from .serializers import NewsSerializer
from .models import News


class Post(ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class PostUpd(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):


class MailingAPIView(APIView):
    queryset = StdUser.objects.filter(**{'news_subscription':True})

    def get(self, request, **extra_kwargs):
        queryset = self.queryset
        for user in queryset.iterator():
            News.mailing(data=user)  
        return Response({'Status':'OK'},status=status.HTTP_200_OK)

def Mailing():
    queryset = StdUser.objects.filter(**{'news_subscription':True})
    for user in queryset.iterator():
        News.mailing(data=user)
    return None
