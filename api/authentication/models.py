import datetime

from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import UserManager
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


class StdUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def create_student(self, email, first_name=None, last_name=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.is_student = True
        user.set_password(password)
        user.date_joined = timezone.now()
        user.last_update = timezone.now()
        user.save(using=self._db)
        return user

    def create_teacher(self, email, first_name=None, last_name=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.is_teacher = True
        user.set_password(password)
        user.date_joined = timezone.now()
        user.last_update = timezone.now()
        user.save(using=self._db)
        return user


# Base user class
class StdUser(AbstractUser):
    objects = StdUserManager()

    email = models.EmailField(max_length=64, blank=False, unique=True)  # ivanov@gmail.com

    date_joined = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    first_name = models.CharField(max_length=64, blank=False, default="")  # Ivan
    last_name = models.CharField(max_length=64, blank=False, default="")  # Ivanov
    patronymic = models.CharField(max_length=64, blank=False, default="")  # Ivanovych
    avatar = models.ImageField(upload_to='static/media/', blank=True, max_length=1000)  # select image
    bio = models.CharField(max_length=512, blank=True, default="")
    date_of_birth = models.DateField(default=timezone.now)

    is_staff = models.BooleanField(default=False)  # staff user non superuser
    is_active = models.BooleanField(default=True)  # can login
    is_admin = models.BooleanField(default=False)  # superuser

    is_student = models.BooleanField('student status', default=False)
    is_teacher = models.BooleanField('teacher status', default=False)

    USERNAME_FIELD = 'email'  # Email as username
    REQUIRED_FIELDS = []

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
        return self.user.email


class Teacher(models.Model):
    user = models.OneToOneField(StdUser, on_delete=models.CASCADE, default="")
    faculty = models.ForeignKey("Faculty", on_delete=models.SET_DEFAULT, default="")

    def __str__(self):
        return self.user.email


class Profession(Group):
    pass


class Faculty(Group):
    pass
