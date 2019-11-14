from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from .serializers import NewsIntSerializer
from .models import NewsInt

class PostInt(CreateAPIView):
    serializer_class = NewsIntSerializer
    queryset = NewsInt.objects.all()

    def get(self, request):
        list = NewsInt.objects.all()
        serializer = NewsIntSerializer(list, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = NewsIntSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostUpdInt(APIView):
    serializer_class = NewsIntSerializer
    queryset = NewsInt.objects.all()
    lookup_field = 'id'

    def get_object(self, id):
        try:
            return NewsInt.objects.get(id=id)
        except NewsInt.DoesNotExist:
            raise Http404

    def get(self, request, id):
        news = self.get_object(id)
        serializer = NewsIntSerializer(news)
        return Response(serializer.data)

    def put(self, request, id):
        news = self.get_object(id)
        serializer = NewsIntSerializer(news, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        news = self.get_object(id)
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)