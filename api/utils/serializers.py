from django.contrib.auth.password_validation import validate_password 

from rest_framework import serializers
from django.contrib.auth import (
        get_user_model, 
        authenticate,)
from django.db.models import Q

from rest_framework.response import Response

from utils.models import Mail
User = get_user_model()

class SendMailSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=64)
    subject = serializers.CharField(max_length=256)
    body = serializers.CharField(max_length=2048)
    
    class Meta(object):
        model = Mail

        fields = '__all__'

    def send(self, data):
        email = data.get('email')
        subject = data.get('subject')
        body = data.get('body')
        return Mail.send_mail(email=email,subject=subject,body=body)


