from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import NewsSerializer
from .models import News


class NewsAPIView(ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class SingleNewsView(RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer