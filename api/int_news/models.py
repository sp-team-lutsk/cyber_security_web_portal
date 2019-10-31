from django.db import models
from authentication.models import StdUser

class News_int(models.Model):

    title = models.CharField(max_length=64, default="", blank=False)
    content = models.TextField(max_length=512, default="", blank=True)
    images = models.ImageField(upload_to='static/media/', blank=True, max_length=1000)
    author = models.ForeignKey(StdUser, on_delete=models.CASCADE)
    date_publication = models.DateTimeField(auto_now=True, auto_now_add=False)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return self.title