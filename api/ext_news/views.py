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

    def get_object(self, pk):
        try:
            return News.objects.get(pk=pk)
        except News.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        news = self.get_object(pk)
        serializer = NewsSerializer(news)
        return Response(serializer.data)

    def put(self, request, pk):
        news = self.get_object(pk)
        serializer = NewsSerializer(news, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        news = self.get_object(pk)
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class MailingAPIView(APIView):
    queryset = StdUser.objects.filter(**{'news_subscription':True})

    def get(self, request, **extra_kwargs):
        queryset = self.queryset
        for user in queryset.iterator():
            News.mailing(data=user)
        return Response({'Status':'OK'},status=status.HTTP_200_OK)

    def mailing():
        queryset = StdUser.objects.filter(**{'news_subscription':True})
        for user in queryset.iterator():
            News.mailing(data=user)
        return None
