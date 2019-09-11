from rest_framework.views import APIView
from rest_framework.generics import (ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from .serializers import NewsSerializer
from .models import News

class Post(CreateAPIView):
    serializer_class = NewsSerializer
    permission_classes = (IsAuthenticated,)
    queryset = News.objects.all()

    def get(self, request):
        list = News.objects.all()
        serializer = NewsSerializer(list, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class News_Details(APIView):
    serializer_class = NewsSerializer
    permission_classes = (IsAuthenticated,)
    queryset = News.objects.all()
    lookup_field = 'pk'

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