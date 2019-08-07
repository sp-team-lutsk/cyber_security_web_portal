from django.db import models
from django.contrib.auth.models import User, Group

# Base user class
class SiteUser(User):
    name = models.CharField(max_length=64, blank=False)             # Ivan
    surname = models.CharField(max_length=64, blank=False)          # Ivanov
    patronymic = models.CharField(max_length=64, blank=False)       # Ivanovych
    avatar = models.ImageField(upload_to='static/images/', blank=True, max_length=1000)     # select image

# Class for groups
class AcademicGroup(models.Model):
    GROUP_CHOICES = (
        ('КБ-11', 'Кiбербезпека 1 курс'),
        ('КБ-21', 'Кiбербезпека 2 курс'),
        ('КБ-31', 'Кiбербезпека 3 курс'),
        ('КБ-41', 'Кiбербезпека 4 курс'),
        ('КСМ-11', 'Комп. системи та мережi 1 курс'),
        ('КСМ-21', 'Комп. системи та мережi 2 курс'),
        ('КСМ-31', 'Комп. системи та мережi 3 курс'),
        ('КСМ-41', 'Комп. системи та мережi 4 курс')
    )

    amount = models.IntegerField(blank=False)                                               # 25
    group_code = models.CharField(max_length=6, choices=GROUP_CHOICES, blank=False)                                # CB-41
    
    # Using 'Student' and 'Teacher' because of cyclic keys
    studens = models.ForeignKey('Student', 
            on_delete=models.CASCADE, 
            related_name="%(app_label)s_%(class)s_related", blank=True)                     # [Ivanov, Petrov, Vasilenko, ...]
    curator = models.OneToOneField('Teacher', on_delete=models.CASCADE, primary_key=True)   # Kotsuba A. U

    # Returns group code (CB-41 for example)
    def __str__(self):
        return(self.group_code)

# Class for students
class Student(Group):
    record_book_code = models.CharField(max_length=8)                               # requires clarification (smth. like 182.10)
    group = models.OneToOneField(Group, 
            on_delete=models.CASCADE, 
            primary_key=True,
            blank=True)                                                             # CB-41    
    language = models.CharField(max_length=24, default="Укр")                       # Ukrainian
    faculty = models.CharField(max_length=64, default="ФКНIТ")                      # FKNIT
    pulpit = models.CharField(max_length=128, default="КIтаКБ")                     # Cathedra of computer systems

# Class for teachers
class Teacher(Group):
    faculty = models.CharField(max_length=64)                                       # FKNIT
    pulpit = models.CharField(max_length=128)                                       # Cathedra of computer systems
