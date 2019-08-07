from django.db import models

# Base user class
class User(models.Model):
    name = models.CharField(max_length=64, blank=False)             # Ivan
    surname = models.CharField(max_length=64, blank=False)          # Ivanov
    patronymic = models.CharField(max_length=64, blank=False)       # Ivanovych
    email = models.EmailField(max_length=64, blank=False)           # ivanov@gmail.com
    password = models.CharField(max_length=64, blank=False)         # 21kjfs23iuk
    avatar = models.ImageField(upload_to='static/images/', blank=True, max_length=1000)     # select image

# Class for groups
class Group(models.Model):
    amount = models.IntegerField(blank=False)                                               # 25
    group_code = models.CharField(max_length=5, blank=False)                                # CB-41
    
    # Using 'Student' and 'Teacher' because of cyclic keys
    studens = models.ForeignKey('Student', 
            on_delete=models.CASCADE, 
            related_name="%(app_label)s_%(class)s_related", blank=True)                     # [Ivanov, Petrov, Vasilenko, ...]
    curator = models.OneToOneField('Teacher', on_delete=models.CASCADE, primary_key=True)   # Kotsuba A. U

    # Returns group code (CB-41 for example)
    def __str__(self):
        return(self.group_code)

# Class for students
class Student(User):
    record_book_code = models.CharField(max_length=8)                               # requires clarification (smth. like 182.10)
    group = models.OneToOneField(Group, 
            on_delete=models.CASCADE, 
            primary_key=True,
            blank=True)                                                             # CB-41    
    language = models.CharField(max_length=24, default="Укр")                       # Ukrainian
    faculty = models.CharField(max_length=64, default="ФКНIТ")                      # FKNIT
    pulpit = models.CharField(max_length=128, default="КIтаКБ")                     # Cathedra of computer systems

# Class for teachers
class Teacher(User):
    faculty = models.CharField(max_length=64)                                       # FKNIT
    pulpit = models.CharField(max_length=128)                                       # Cathedra of computer systems
