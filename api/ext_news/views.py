from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NewsSerializer
from .models import News


class NewsAPIView(APIView):
    def get(self, request):
        articles = News.objects.all()
        serializer = NewsSerializer(articles, many=True)
        return Response({"news": serializer.data})
    def post(self, request):
        news = request.data.get('news')
        # Create an article from the above data
        serializer = NewsSerializer(data=news)
        if serializer.is_valid(raise_exception=True):
            new_saved = serializer.save()
        return Response({"success": "News '{}' created successfully".format(new_saved.title)})
