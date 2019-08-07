from django.contrib import admin
from .models import Student, Teacher, AcademicGroup

all_models = [Student, Teacher, AcademicGroup]

admin.site.register(all_models)
