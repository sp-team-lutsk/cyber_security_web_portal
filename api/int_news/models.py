from django.db import models

class News_int(models.Model):
    title = models.CharField(max_length=64, default="", blank=False)
    content = models.TextField(max_length=512, default="", blank=True)
    images_link = models.URLField(default="", blank=True)
   #author = models.ForeignKey(User)
    date_publication = models.DateTimeField(auto_now=True, auto_now_add=False)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return self.title