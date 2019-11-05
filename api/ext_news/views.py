from django.contrib.auth import get_user_model  
from rest_framework import status
from rest_framework.generics import  GenericAPIView, ListCreateAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.views import APIView

from rest_framework.response import Response

from authentication.permissions import AllowAny, IsModeratorUser
from ext_news.serializers import NewsSerializer, SetNewsSerializer
from ext_news.models import News
from utils.decorators import permission


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
        return self.delete(request, *args, **kwargs)

class SetNews(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = NewsSerializer
    queryset = News.objects.none()

    @permission("IsModeratorUser") 
    def post(self, request, *args, **kwargs):
        self.serializer_class = SetNewsSerializer
        news = News.objects.filter(id=request.data.get('id'),is_checked = False)
        serializer = self.serializer_class(news , data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response(data={"is_checked": "News '{}' validated".format(str(news))},
                status=status.HTTP_200_OK)
        
