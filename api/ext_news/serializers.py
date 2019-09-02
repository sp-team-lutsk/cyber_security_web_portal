from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = News
        fields = ('title', 'discription', 'news_link', 'images_link', 'is_checked',)

        def create(self, validated_data):
            return News.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.title = validated_data.get('title', instance.title)
            instance.description = validated_data.get('description', instance.description)
            instance.news_link = validated_data.get('news_link', instance.news_link)
            instance.images_link = validated.data.get('images_link', instance.images_link)
            instance.save()
            return instance