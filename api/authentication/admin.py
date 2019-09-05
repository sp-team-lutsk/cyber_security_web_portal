from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from allauth.socialaccount.models import SocialAccount 
from .models import StdUser, Profession, Faculty, Student, Teacher

class StudentInline(admin.TabularInline):
    model = Student
    extra = 0

class TeacherInline(admin.TabularInline):
    model = Teacher
    extra = 0

class SocialUserInline(admin.TabularInline):
    model = SocialAccount
    extra = 0

class StdUserAdmin(UserAdmin):
    model = StdUser

    ordering = ('email', )
    list_display = ('email', 'is_staff', 'is_active', 'is_teacher', 'is_student')
    list_filter = ('email',)
    readonly_fields = ('date_joined', 'token', 'last_update', 'is_staff', 'is_superuser',)
    inlines = [SocialUserInline, StudentInline, TeacherInline,]

    fieldsets = (
            ('Active status', {
                'fields': ('is_active',)
            }),
            ('Personal Info', {
                'fields': ('email',
                           'password', 
                           'first_name', 
                           'last_name',
                           'patronymic',
                           'bio',
                           'avatar',
                           'token',)
                }),
            ('Permissions', {
                'fields': ('is_staff',
                           'is_superuser',
                           'is_student',
                           'is_teacher',
                           'user_permissions',)
                }),
            ('Important Dates', {
                'fields': ('date_of_birth',
                           'date_joined',
                           'last_update',)
                }),
    )

    add_fieldsets = (
            (None, {
                'classes': ('wide', ),
                'fields': ('email',
                           'password1',
                           'password2',)
            }),
    )

admin.site.register(StdUser, StdUserAdmin)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Profession)
admin.site.register(Faculty)
