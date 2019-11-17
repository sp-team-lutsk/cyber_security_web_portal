from django.http import Http404
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

class PostUpd(APIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def get_object(self, id):
        try:
            return News.objects.get(id=id)
        except News.DoesNotExist:
            raise Http404

    def get(self, request, id):
        news = self.get_object(id)
        serializer = NewsSerializer(news)
        return Response(serializer.data)

    def put(self, request, id):
        news = self.get_object(id)
        serializer = NewsSerializer(news, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        news = self.get_object(id)
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



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
