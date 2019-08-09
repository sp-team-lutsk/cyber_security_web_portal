import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


# Base user class
class StdUser(AbstractUser):
    email = models.EmailField(max_length=64, blank=False, unique=True) # ivanov@gmail.com
    
    date_joined = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    
    username = models.CharField(max_length=18, blank=False, unique=True) # Azrael
    first_name = models.CharField(max_length=64, blank=False)            # Ivan
    last_name = models.CharField(max_length=64, blank=False)             # Ivanov
    patronymic = models.CharField(max_length=64, blank=False)            # Ivanovych
    avatar = models.ImageField(upload_to='static/images/', blank=True, max_length=1000)     # select image
    bio = models.CharField(max_length=256, blank=True)
    date_of_birth = models.DateField(default=timezone.now)

    is_staff = models.BooleanField(default=False) # staff user non superuser
    active = models.BooleanField(default=True) # can login
    admin = models.BooleanField(default=False) # superuser

    USERNAME_FIELD = 'email' # Email as username
    # USERNAME_FIELD and password are required by default

    REQUIRED_FIELDS = ['username']

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_full_name(self):
        """ Returns full name with spaces between """
        full_name = "%s %s %s" % (self.first_name, self.last_name, self.patronymic)
        return full_name.strip()

    def get_short_name(self):
        """ Returns short name """
        short_name = "%s" % (self.first_name)
        return short_name.strip()
    
    def email_user(self):
        """ Send email to user """
        pass

    def get_avatar(self):
        """ Returns avatar (use Pillow) """
        pass

    # Saving
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    # Commented for tests
    # Abstract class
    # class Meta:
    #    abstract = True 
