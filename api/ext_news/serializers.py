from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = News
        fields = ('id', 'title', 'description', 
                'news_link', 'images_link', 'is_checked',)


class SetNewsSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(
    choices=['False', 'True'],)
    class Meta(object):
        model = News
        fields = ('id', 'status',)
