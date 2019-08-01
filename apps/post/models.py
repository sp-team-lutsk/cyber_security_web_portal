from django.db import models

class Post(models.Model):
   title = models.CharField(max_length=30)
   url =  models.CharField(max_length=30)
   image = models.ImageField(upload_to='static/images/', blank=True, max_length=1000)
   text = models.CharField(max_length=3000)


class Meta:
   abstract = True