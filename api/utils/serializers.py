from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class SendMailSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=64)
    subject = serializers.CharField(max_length=256)
    body = serializers.CharField(max_length=2048)
    
    class Meta(object):
        model = None

        fields = ('email',
                  'subject',
                  'body',)

    def send(self, data):
        email = data.get('email')
        subject = data.get('subject')
        body = data.get('body')
        return send_mail(email=email, subject=subject, body=body)


class MassMailSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(max_length=256)
    body = serializers.CharField(max_length=2048) 
    
    class Meta(object):
        model = User
        fields = (
                'subject',
                'body',
                'is_active',
                'is_student',
                'is_teacher',
                'is_moderator',
                'is_admin',)

