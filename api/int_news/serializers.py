from rest_framework import serializers
from .models import News_int

class News_int_Serializer(serializers.ModelSerializer):

    class Meta(object):
        model = News_int
        fields = ('title', 'content', 'author', 'date_created', 'date_publication', 'images', 'is_checked',)

