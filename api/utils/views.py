from django.conf import settings 
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.views import APIView

from authentication.permissions import (IsAdminUser, 
                        IsAuthenticated, 
                        IsModeratorUser,
                        IsStaffUser,
                        AllowAny)

from rest_framework.response import Response

from authentication.models import StdUser
from ext_news.models import News
from utils.serializers import (
    SendMailSerializer,
    MassMailSerializer,
   )
from utils.decorators import permission, permissions, object_permission

User = get_user_model()



class SendMailAPIView(APIView):
    """
    Send mail from admin to user
    """
    serializer_class = SendMailSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    
    def post(self, request):
        serializer = SendMailSerializer(data=request.data)
        user = self.queryset.get(email=request.data.get('email'))
        if user is not None:
            if serializer.is_valid(raise_exception=True):
                serializer.send(data=request.data)
                return Response({'Status': 'Mail Send'}, status=status.HTTP_200_OK)

class MailingAPIView(APIView):
    permission_classes = [AllowAny, ]
    queryset = StdUser.objects.filter(news_subscription = True)

    def get(self, request, **extra_kwargs):
        queryset = self.queryset
        for user in queryset.iterator():
            news_mailing(data=user)  
        return Response({'Status':'OK'},status=status.HTTP_200_OK)

class ModeratorMailAPIView(APIView):
    permission_classes = [AllowAny, ]
    queryset = User.objects.none()
    
    @permission("IsModeratorUser")
    def post(self, request, *args, **kwargs):
        self.serializer_class = MassMailSerializer
        serializer = MassMailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            obj = request.data.copy()
            MassMailing(obj)
            return Response({'Mails':'Sent'},status=status.HTTP_200_OK)
        else:
            return Response({'Mails':'failed'})

def MassMailing(obj):
    users = []
    if obj.get('is_active') != None:
        users = list(StdUser.objects.filter(is_active = True))
    if obj.get('is_student') != None:
        users = users + list(StdUser.objects.filter(is_moderator = True))
    if obj.get('is_teacher') != None:
        users = users + list(StdUser.objects.filter(is_moderator = True))
    if obj.get('is_moderator') != None:
        users = users + list(StdUser.objects.filter(is_moderator = True))
    if obj.get('is_admin') != None:
        users = users + list(StdUser.objects.filter(is_moderator = True))

    for user in users:
        send_mail(email = user.email,
                  subject=obj.get('subject'), 
                  body = obj.get('body'))
    return None

def news_subscription():
    queryset = StdUser.objects.filter(news_subscription = True)
    for user in queryset.iterator():
        news_mailing(data=user)
    return None

def news_mailing(data):
    queryset = list(News.objects.all()[:3])
    context = {'user': data.email, 
               'data': queryset,
               }
    msg = EmailMessage(subject='Новини за тиждень',
                       body=render_to_string('ext_news/mail/mail.html',context), 
                       to=[data.email])
    msg.content_subtype = 'html'
    msg.send()

def send_mail(email, subject, body):
    msg = EmailMessage(subject=subject,
                       body=body,
                       to=[email])
    msg.content_subtype = 'html'
    msg.send()
