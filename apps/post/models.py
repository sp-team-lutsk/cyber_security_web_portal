from django.db import models

# Class for Post abstraction
class Post(models.Model):
   title = models.CharField(max_length=30)      # Article title
   url =  models.CharField(max_length=30)       # Url to original article
   
   # Image for article
   image = models.ImageField(upload_to='static/images/', blank=True, max_length=1000)
   text = models.CharField(max_length=3000)     # Article main text

    # Return title, when object used by name
    def __str__(self):
        return self.title

    # Class is abstact. Good for inheritance
    class Meta:
        abstract = True
