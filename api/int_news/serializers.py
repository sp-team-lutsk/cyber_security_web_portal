from rest_framework import serializers
from .models import NewsInt


class NewsIntSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = NewsInt
        fields = ('id', 'title', 'content', 
                'author', 'date_created', 'published_date',
                'images', 'is_checked',)

    def create(self, validated_data):
        return NewsInt.objects.create(**validated_data)

    def delete(self, u):
        u.is_active = False
        u.save()

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.author = validated_data.get('author', instance.author)
        instance.published_date= validated_data.get('date_publication', instance.published_date)
        instance.images = validated_data.get('images', instance.images)
        instance.is_checked = validated_data.get('is_checked', instance.is_checked)
        instance.save()
        return instance
