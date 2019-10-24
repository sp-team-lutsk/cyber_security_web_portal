from django.db import models

class News_int(models.Model):
    title = models.CharField(max_length=64, default="", blank=False)
    description = models.TextField(max_length=512, default="", blank=True)
    news_link = models.URLField(default="", blank=True)
    images_link = models.URLField(default="", blank=True)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return self.title