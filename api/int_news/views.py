from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from int_news.serializers import NewsIntSerializer
from int_news.models import NewsInt
from utils.decorators import permission, permissions
from ext_news.serializers import SetNewsSerializer
from utils.permissions import AllowAny
from utils.views import get_int_news

class PostUpdInt(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = NewsIntSerializer
    queryset = NewsInt.objects.all()
    lookup_field = 'id'

    def get(self, request, id,*args, **kwargs):
        news = get_int_news(id)
        serializer = NewsIntSerializer(news)
        return Response(serializer.data)

    def put(self, request, id,*args, **kwargs):
        news = get_int_news(id)
        serializer = NewsIntSerializer(news, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        news = get_int_news(id)
        news.delete()
        return Response({'Status': 'OK'}, status=status.HTTP_200_OK)


class News_Bulk(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = NewsIntSerializer
    queryset = NewsInt.objects.none()

    def get(self, request, *args, **kwargs):
        news = NewsInt.objects.all()
        serializer = NewsIntSerializer(news, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        self.serializer_class = NewsIntSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        news_saved = serializer.save()
        return Response(
            data={"success": "News '{}' created successfully".format((news_saved))},
            status=status.HTTP_201_CREATED)


    def put(self, request, *args, **kwargs):
        self.serializer_class = NewsIntSerializer
        queryset = NewsInt.objects.all()
        for nev in list(queryset):
            serializer = NewsIntSerializer(nev, data=request.data)
            if serializer.is_valid():
                serializer.save()

        return Response(data={"200": "OK"}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        news = NewsInt.objects.all()
        news.delete()
        return Response({'Status': 'OK'},status=status.HTTP_200_OK)


class ModeratorCheckNewsAPIView(APIView):
    queryset = NewsInt.objects.none()
    permission_classes = [AllowAny, ]
    serializer_class = SetNewsSerializer

    def post(self, request, *args, **kwargs):
        try:
            news = NewsInt.objects.get(id=request.data.get('id'))
            serializer = self.serializer_class(news, data=request.data)
            check = request.data.get('status')
            news.is_checked = check
            news.save()
            return Response(data={"is_checked": "{}".format(str(check))}, status=status.HTTP_200_OK)
        except:
            return Response(data={"News": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
