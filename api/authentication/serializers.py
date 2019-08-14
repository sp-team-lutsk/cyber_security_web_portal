from rest_framework import serializers
from django.contrib.auth import get_user_model 
 
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()
 
    class Meta(object):
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'date_joined',
            'password'
        )
        extra_kwargs = {'password': {'write_only': True}}
