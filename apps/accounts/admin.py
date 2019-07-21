from django.contrib import admin
from .models import Student, Teacher, Group

all_models = [Student, Teacher, Group]

admin.site.register(all_models)
