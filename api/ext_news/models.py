from django.db import models

class News(models.Model):
    title = models.CharField(max_length=200)
    discription = models.TextField()
    news_link = models.URLField()
    images_link = models.ImageField(upload_to='ext_news')
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return self.title
