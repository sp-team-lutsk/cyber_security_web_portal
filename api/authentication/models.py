import datetime

from django.template.loader import render_to_string
from django.db import models
from django.utils import timezone
from django.core.signing import (TimestampSigner, 
        b64_encode, 
        b64_decode, 
        BadSignature,
        force_bytes)
from django.core.mail import EmailMessage
from django.contrib.auth.models import UserManager, AbstractUser, Group
from django.conf import settings 

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

USER_TYPES = {
    "ADMIN": 1,
    "MODERATOR": 2,
    "USER": 3,
}


class StdUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        return self._create_user(email, password, **extra_fields)

    def create_user(self, email, password=None, user_type=3, **extra_fields):
        if user_type == USER_TYPES["USER"]:
            extra_fields.setdefault('is_moderator', False)
            extra_fields.setdefault('is_admin', False)
            extra_fields.setdefault('is_active', False)

        elif user_type == USER_TYPES["ADMIN"]:
            extra_fields.setdefault('is_admin', True)
            extra_fields.setdefault('is_active', True)
        
        elif user_type == USER_TYPES["MODERATOR"]:
            extra_fields.setdefault('is_moderator', True)
            extra_fields.setdefault('is_active', True)

        return self._create_user(email, password, **extra_fields)

    def create_student(self, email, profession, faculty, password=None): 
        if not email:
            raise ValueError("Email must be set")


        user = self.model(
            email=self.normalize_email(email),
        )
        
        try:
            profession = Profession.objects.get(name=profession.name)
            faculty = Faculty.objects.get(name=faculty.name)
        except:
            raise ValueError('Not found such object')

        user.is_student = True
        user.set_password(password)

        user.date_joined = timezone.now()
        user.last_update = timezone.now()
        user.save(using=self._db)
        
        student = Student.objects.create(user=user, profession=profession, faculty=faculty)
        student.save()

        return user

    def create_teacher(self, email, faculty, password=None):
        if not email:
            raise ValueError("Email must be set")

        user = self.model(
            email=self.normalize_email(email),
        )

        try:
            faculty = Faculty.objects.get(name=faculty.name)
        except:
            raise ValueError('Not found such object')

        user.is_teacher = True
        user.set_password(password)
        
        user.date_joined = timezone.now()
        user.last_update = timezone.now()
        user.save(using=self._db)

        Teacher.objects.create(user=user, faculty=faculty)

        return user


# Base user class
class StdUser(AbstractUser):
    objects = StdUserManager()

    # We need this, because in AbstractUser 'unique=True'
    username = models.CharField(max_length=64, blank=True, unique=False)
    email = models.EmailField(max_length=64, blank=False, unique=True)  # ivanov@gmail.com

    date_joined = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    first_name = models.CharField(max_length=64, blank=False, default="")  # Ivan
    last_name = models.CharField(max_length=64, blank=False, default="")  # Ivanov
    patronymic = models.CharField(max_length=64, blank=True, default="")  # Ivanovych
    avatar = models.ImageField(upload_to='static/media/', blank=True, max_length=1000)  # select image
    bio = models.CharField(max_length=512, blank=True, default="")
    date_of_birth = models.DateTimeField(default=timezone.now)
    gender = models.CharField(max_length=64, blank=True, default="man") # Man/Wpman
    
    news_subscription = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)  # can login
    is_admin = models.BooleanField(default=False)  # admin
    is_moderator = models.BooleanField(default=False) # moderator

    is_student = models.BooleanField('student status', default=False)
    is_teacher = models.BooleanField('teacher status', default=False)
    
    code = models.CharField(max_length=256, blank=True, default="")
    USERNAME_FIELD = 'email'  # Email as username
    REQUIRED_FIELDS = []
    
    class Meta:
        permissions = [('read_news', 'Читати новини',),]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_full_name(self):
        """ Returns full name with spaces between """
        full_name = "%s %s %s" % (self.first_name, self.last_name, self.patronymic)
        return full_name.strip()

    def get_short_name(self):
        """ Returns short name """
        short_name = "%s" % self.first_name
        return short_name.strip()

    def get_verification_code(self, email):
        # verification token 
        signer = TimestampSigner()
        return b64_encode(bytes(signer.sign(email), encoding='utf-8'))
        
    @classmethod
    def verify_email(self, code):
        if code:
            signer = TimestampSigner()
            try:
                code = code.encode('utf-8')
                max_age = datetime.timedelta(days=settings.VERIFICATION_CODE_EXPIRED).total_seconds()
                code = force_bytes(code)
                code = b64_decode(code)
                code = code.decode()
                email = signer.unsign(code, max_age=max_age)
                user = StdUser.objects.get(**{StdUser.USERNAME_FIELD: email, 'is_active': False})
                user.is_active = True
                user.code = "None code"
                user.save()
                
                return True, ('Your account has been activated.')  
            except (BadSignature, StdUser.DoesNotExist, TypeError, UnicodeDecodeError):
                raise ValueError('Error')
            return False, ('Activation link is incorrect, please resend request')
        else:
            raise ValueError('No code')

    @classmethod
    def verify_password(self, code, password):
        if code:
            signer = TimestampSigner()
            try:
                code = code.encode('utf-8')
                max_age = datetime.timedelta(days=settings.VERIFICATION_CODE_EXPIRED).total_seconds()
                code = force_bytes(code)
                code = b64_decode(code)
                code = code.decode()
                email = signer.unsign(code, max_age=max_age)
                 
                user = StdUser.objects.get(**{StdUser.USERNAME_FIELD: email})
                user.set_password(password)
                user.code = 'None code'
                user.save()
                return True
            except (BadSignature, AttributeError, StdUser.DoesNotExist, TypeError, UnicodeDecodeError):
                raise ValueError('Error')
            return False, ('Activation link is incorrect, please resend request')
        else:
            raise ValueError('No code')

    def send_mail(self, email):
        verification_code = self.get_verification_code(email=email)
        context = {'user': self,
                   'VERIFICATION_URL': settings.VERIFICATION_URL,
                   'HOST': settings.ALLOWED_HOSTS[0],
                   'code': verification_code.decode(),
                   'link': datetime.datetime.today() + datetime.timedelta(days=settings.VERIFICATION_CODE_EXPIRED)   
                }
        
        msg = EmailMessage(subject='subject',
                body=render_to_string('authentication/mail/verification_body.html', context),
                to=[email])
        msg.content_subtype = 'html'
        msg.send()

    def send_recovery_password(self, email):
        verification_code = self.get_verification_code(email=email)
        
        context = {'user': self,
                   'RECOVER_URL': settings.RECOVER_URL,
                   'HOST': settings.ALLOWED_HOSTS[0],
                   'code': verification_code.decode(),
                   'link': datetime.datetime.today() + datetime.timedelta(days=settings.RECOVER_CODE_EXPIRED)
                    }
        msg = EmailMessage(subject='subject',
                body=render_to_string('authentication/mail/reset_body.html', context),
                to=[email])
        msg.content_subtype = 'html'
        msg.send()

    # Saving
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Student(models.Model):
    user = models.OneToOneField(StdUser, on_delete=models.CASCADE, default="")
    profession = models.ForeignKey('Profession', on_delete=models.SET_DEFAULT, default="")
    faculty = models.ForeignKey("Faculty", on_delete=models.SET_DEFAULT, default="")
    acad_group = models.CharField(max_length=256, choices=ACAD_GROUPS_CHOICES, default="")  
    class Meta:
        permissions = [('write_to_teacher', 'Писати викладачу'),]


class Teacher(models.Model):
    user = models.OneToOneField(StdUser, on_delete=models.CASCADE, default="")
    faculty = models.ForeignKey("Faculty", on_delete=models.SET_DEFAULT, default="")

    class Meta:
        permissions = [('add_post', 'Створити пост'),
                       ('edit_post', 'Змiнювати пост'),
                       ('delete_post', 'Видалити пост'),
                       ('change_student_perm', 'Змiнювати права стундентiв'),]


class Profession(Group):
    pass


class Faculty(Group):
    pass
