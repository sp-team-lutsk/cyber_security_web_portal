from django.http import Http404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from authentication.permissions import AllowAny
from ext_news.serializers import NewsSerializer, SetNewsSerializer
from ext_news.models import News
from utils.decorators import permission


class Post(ListCreateAPIView):
    queryset = News.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = NewsSerializer


class PostUpd(APIView):
    queryset = News.objects.all()
    permission_classes = [AllowAny, ]
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

class ModeratorCheckNewsAPIView(APIView):
    queryset = News.objects.none()
    permission_classes = [AllowAny, ]
    serializer_class = SetNewsSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            news = News.objects.get(id=request.data.get('id'))
            serializer = self.serializer_class(news, data = request.data)
            news.is_checked = True
            news.save()
            return Response(data={"is_checked": "True"},status=status.HTTP_200_OK)
        except:
            return Response(data={"News": "Not Found"},status=status.HTTP_404_NOT_FOUND)
