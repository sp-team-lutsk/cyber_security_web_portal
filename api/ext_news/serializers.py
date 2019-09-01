from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = News
        fields = ('title', 'discription', 'news_link', 'images_link', 'is_checked',)
        author_id = serializers.IntegerField()

        def create(self, validated_data):
            return News.objects.create(**validated_data)
