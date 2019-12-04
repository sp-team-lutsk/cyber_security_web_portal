from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from utils.permissions import (IsAdminUser, AllowAny)

from authentication.models import StdUser
from ext_news.models import News
from utils.serializers import (
    SendMailSerializer,
    MassMailSerializer,
   )
from utils.decorators import permission

User = get_user_model()


"""
get_ functions for raise DoesNotExist error
"""
def get_user(arg):
    try:
        return StdUser.objects.get(id=arg)
    except ValueError: 
        return StdUser.objects.get(email=arg)
    except DoesNotExist:
        return Response(data={"User":"DoesNotExist"},status=status.HTTP_404_NOT_FOUND)

def get_ext_news(arg):
    try:
        return News.objects.get(id=arg)
    except News.DoesNotExist:
        return Response(data={"Ext News":"DoesNotExist"},status=status.HTTP_404_NOT_FOUND)

def get_int_news(arg):
    try:
        return NewsInt.objects.get(id=arg)
    except NewsInt.DoesNotExist:
        return Response(data={"Int News":"DoesNotExist"},status=status.HTTP_404_NOT_FOUND)


class SendMailAPIView(APIView):
    """
    Send mail from admin to user
    """
    serializer_class = SendMailSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.none()

    @permission("IsModeratorUser")
    def post(self, request,*args,**kwargs):
        serializer = SendMailSerializer(data=request.data)
        user = get_user(request.data.get('email'))
        send_mail(email=request.data.get('email'),
                  subject=request.data.get('subject'),
                  body=request.data.get('body'))
        return Response({'Status': 'Mail Send'}, status=status.HTTP_200_OK)


class MailingAPIView(APIView):
    permission_classes = [AllowAny, ]
    queryset = StdUser.objects.filter(news_subscription=True)

    def get(self, request, **extra_kwargs):
        queryset = self.queryset
        for user in queryset.iterator():
            news_mailing(data=user)
        return Response({'Status': 'OK'}, status=status.HTTP_200_OK)


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
            return Response({'Mails': 'Sent'}, status=status.HTTP_200_OK)
        else:
            return Response({'Mails': 'failed'})


def MassMailing(obj):
    users = []
    if obj.get('is_active') != None:
        users = list(StdUser.objects.filter(is_active=True))
    if obj.get('is_student') != None:
        users = users + list(StdUser.objects.filter(is_moderator=True))
    if obj.get('is_teacher') != None:
        users = users + list(StdUser.objects.filter(is_moderator=True))
    if obj.get('is_moderator') != None:
        users = users + list(StdUser.objects.filter(is_moderator=True))
    if obj.get('is_admin') != None:
        users = users + list(StdUser.objects.filter(is_moderator=True))

    for user in users:
        send_mail(email=user.email,
                  subject=obj.get('subject'),
                  body=obj.get('body'))
    return None


def news_subscription():
    queryset = StdUser.objects.filter(news_subscription=True)
    for user in queryset.iterator():
        news_mailing(data=user)
    return None


def news_mailing(data):
    queryset = list(News.objects.all()[:3])
    context = {'user': data.email,
               'data': queryset,
               }
    msg = EmailMessage(subject='Новини за тиждень',
                       body=render_to_string('/utils/mail/news_mail.html', context),
                       to=[data.email])
    msg.content_subtype = 'html'
    msg.send()


def send_mail(email, subject, body):
    context = {'body': body,
               'user': get_user(email),
               'subject': subject,
               }
    msg = EmailMessage(subject=subject,
            body=render_to_string('utils/mail/single_mail.html', context),
                       to=[email])
    msg.content_subtype = 'html'
    msg.send()



