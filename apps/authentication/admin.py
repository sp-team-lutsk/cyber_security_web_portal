from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Student, Teacher, AcademicGroup

class StudentProfileInline(admin.StackedInline):
    model = Student
    can_delete = False

    
class TeacherProfileInline(admin.StackedInline):
    model = Teacher
    can_delete = False
  

class AcademicGroupProfileInline(admin.StackedInline):
    model = AcademicGroup
    can_delete = False


class StudentAdmin(UserAdmin):
    inlines = (UserProfileInline, )

    
class TeacherAdmin(UserAdmin):
    inlines = (UserProfileInline, )

    
class AcademicGroupAdmin(UserAdmin):
    inlines = (UserProfileInline, )

    
admin.site.unregister(User)

admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(AcademicGroup, AcademicGroupAdmin)
