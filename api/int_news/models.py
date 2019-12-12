from django.db import models
from django.utils import timezone
from authentication.models import StdUser

STATUS = (
        (0, "Draft"),
        (1, "Publish")
    )

class NewsInt(models.Model):
    title = models.CharField(max_length=64, default="", blank=False)
    content = models.TextField(max_length=512, default="", blank=True)
    images = models.ImageField(upload_to='static/media/', blank=True, null=True, max_length=1000)
    author = models.ForeignKey(StdUser, on_delete=models.CASCADE, blank=True)
    published_date = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    is_checked = models.BooleanField(default=False)

    def publish(self):
        date = timezone.now()
        self.published_date = date
        self.save()

        return date

    class Meta:
        ordering = ['-date_created']
