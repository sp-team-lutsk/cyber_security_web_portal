from rest_framework import viewsets
from .serializers import NewsSerializer
from .models import News

class Post(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

