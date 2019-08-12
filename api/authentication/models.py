import datetime

from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group

ACAD_GROUPS_CHOICES = [
    ("КБ-11", "Кiбербезпека 1 курс"),
    ("КБ-21", "Кiбербезпека 2 курс"),
    ("КБ-31", "Кiбербезпека 3 курс"),
    ("КБ-41", "Кiбербезпека 4 курс"),
    ("КСМ-11", "Комп'ютерні системи і мережі 1 курс"),
    ("КСМ-21", "Комп'ютерні системи і мережі 2 курс"),
    ("КСМ-31", "Комп'ютерні системи і мережі 3 курс"),
    ("КСМ-41", "Комп'ютерні системи і мережi 4 курс"),
    ("КСМс-11", "Комп'ютерні системи і мережі 1 курс (скорочений)"),
    ("КСМс-21", "Комп'ютерні системи і мережі 2 курс (скорочений)"),
]


# Base user class
class StdUser(AbstractUser):
    email = models.EmailField(max_length=64, blank=False, unique=True)  # ivanov@gmail.com

    date_joined = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    username = models.CharField(max_length=64, blank=False, unique=True)  # Azrael
    first_name = models.CharField(max_length=64, blank=False)  # Ivan
    last_name = models.CharField(max_length=64, blank=False)  # Ivanov
    patronymic = models.CharField(max_length=64, blank=False)  # Ivanovych
    avatar = models.ImageField(upload_to='static/images/', blank=True, max_length=1000)  # select image
    bio = models.CharField(max_length=512, blank=True)
    date_of_birth = models.DateField(default=timezone.now)

    is_staff = models.BooleanField(default=False)  # staff user non superuser
    active = models.BooleanField(default=True)  # can login
    admin = models.BooleanField(default=False)  # superuser

    is_student = models.BooleanField('student status', default=False)
    is_teacher = models.BooleanField('teacher status', default=False)

    USERNAME_FIELD = 'email'  # Email as username
    REQUIRED_FIELDS = ['username']

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def authenticate(self):
        pass

    def get_full_name(self):
        """ Returns full name with spaces between """
        full_name = "%s %s %s" % (self.first_name, self.last_name, self.patronymic)
        return full_name.strip()

    def get_short_name(self):
        """ Returns short name """
        short_name = "%s" % self.first_name
        return short_name.strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_avatar(self):
        """ Returns avatar (use Pillow) """
        pass

    # Saving
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Student(models.Model):
    user = models.OneToOneField(StdUser, on_delete=models.CASCADE, default="")
    profession = models.ForeignKey('Profession', on_delete=models.SET_DEFAULT, default="")
    faculty = models.ForeignKey("Faculty", on_delete=models.SET_DEFAULT, default="")

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    user = models.OneToOneField(StdUser, on_delete=models.CASCADE, default="")
    faculty = models.ForeignKey("Faculty", on_delete=models.SET_DEFAULT, default="")

    def __str__(self):
        return self.user.username


class Profession(Group):
    pass


class Faculty(Group):
    pass
