from django.db import models
from django.utils import timezone
from authentication.models import StdUser


class NewsInt(models.Model):

    title = models.CharField(max_length=64, default="", blank=False)
    content = models.TextField(max_length=512, default="", blank=True)
    images = models.ImageField(upload_to='static/media/', blank=True, null=True, max_length=1000)
    author = models.ForeignKey(StdUser, on_delete=models.CASCADE,blank=True)
    date_publication = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    is_checked = models.BooleanField(default=False)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title
