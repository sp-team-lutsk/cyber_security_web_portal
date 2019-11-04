import datetime
import jwt

from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.core.signing import TimestampSigner, b64_encode,b64_decode, BadSignature, SignatureExpired,force_bytes
from django.core.mail import EmailMessage
from django.conf import settings 

from ext_news.models import News

class Mail(models.Model):
    email = models.EmailField(max_length=64, blank=False, unique=False)
    subject = models.CharField(max_length=256, blank=False, unique=False)
    body = models.CharField(max_length=2048, blank=False, unique=False)

    @classmethod
    def send_mail(self, email, subject, body):
        
        msg = EmailMessage(subject=subject,
                body=body,
                to=[email])
        msg.content_subtype = 'html'
        msg.send()

    @classmethod
    def mailing(self, data):
        queryset = list(News.objects.all()[:3])
        context = {
                'user': data.email, 
                'data': queryset
                }
        msg = EmailMessage(subject='Новини за тиждень',
                body=render_to_string('ext_news/mail/mail.html',context), 
                to=[data.email])
        msg.content_subtype = 'html'
        msg.send() 
