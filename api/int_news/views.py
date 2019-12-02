from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from int_news.serializers import NewsIntSerializer
from int_news.models import NewsInt




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


class News_Bulk(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = NewsIntSerializer
    queryset = NewsInt.objects.none()

    def get(self, request, *args, **kwargs):
        self.queryset = NewsInt.objects.all()
        return self.list(request, *args, **kwargs)

    def post(self, request):
        self.serializer_class = NewsIntSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        news_saved = serializer.save()
        return Response(
            data={"success": "News '{}' created successfully".format(str(news_saved))},
            status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        self.serializer_class = NewsIntSerializer
        queryset = NewsInt.objects.all()
        for nev in list(queryset):
            serializer = NewsIntSerializer(nev, data=request.data)
            if serializer.is_valid():
                serializer.save()
        return Response(data={"200": "OK"}, status=status.HTTP_200_OK)

    @permission("IsModeratorUser")
    def delete(self, request, *args, **kwargs):
        self.queryset = NewsInt.objects.all()
        self.serializer_class = NewsIntSerializer
        q = list(self.queryset)
        for u in q:
            serializer = self.serializer_class(request.user, data=request.data)
            serializer.delete(u)
        return Response({'Status': 'OK'}, status=status.HTTP_200_OK)


class ModeratorCheckNewsAPIView(APIView):
    queryset = News.objects.none()
    permission_classes = [AllowAny, ]
    serializer_class = SetNewsSerializer

    def post(self, request, *args, **kwargs):
        try:
            news = News.objects.get(id=request.data.get('id'))
            serializer = self.serializer_class(news, data=request.data)
            check = request.data.get('status')
            news.is_checked = check
            news.save()
            return Response(data={"is_checked": "{}".format(str(check))}, status=status.HTTP_200_OK)
        except:
            return Response(data={"News": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
