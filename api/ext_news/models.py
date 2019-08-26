from django.db import models

class news(models.Model):
    title = models.CharField(max_length=200, unique=True)
    discription = models.CharField(max_length=300, unique=True)
    news_link = models.URLField()
    images_link = models.ImageField(upload_to='/ext_news/')