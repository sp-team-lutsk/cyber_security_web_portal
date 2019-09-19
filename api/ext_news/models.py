from django.db import models
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
class News(models.Model):
    title = models.CharField(max_length=200)
    discription = models.TextField()
    news_link = models.URLField()
    images_link = models.ImageField(upload_to='ext_news')
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @classmethod
    def mailing(self, data):
        queryset = list(News.objects.all()[:3])
        context = {
                'user': data.email, 
                'data': queryset
                #'user': data,
                #'title': title,
                #'discription': discription,
                #'news_link': news_link,
                #'images_link': images_link
                }
        msg = EmailMessage(subject='Новини за тиждень',
                body=render_to_string('ext_news/mail/mail.html',context), 
                to=[data.email])
        msg.content_subtype = 'html'
        msg.send() 
