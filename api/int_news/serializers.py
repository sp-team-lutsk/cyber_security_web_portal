from rest_framework import serializers
from .models import NewsInt

class NewsIntSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = NewsInt
        fields = ('title', 'content', 'author', 'date_created', 'date_publication', 'images', 'is_checked',)

