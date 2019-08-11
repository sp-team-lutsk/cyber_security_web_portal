from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import StdUser, Person

class StdUserAdmin(UserAdmin):
    model = StdUser

    list_display = ('email', 'username', 'is_staff', 'is_active',)
    list_filter = ('email',)
    readonly_fields = ('date_joined', 'last_update', 'is_staff', 'is_active', 'is_admin',)
    
    fieldsets = (
            ('Personal Info', {
                'fields': ('email',
                           'username', 
                           'password', 
                           'first_name', 
                           'last_name',
                           'patronymic',
                           'bio',
                           'avatar',)
                }),
            ('Permissions', {
                'fields': ('is_active',
                           'is_staff',
                           'is_admin',)
                }),
            ('Important Dates', {
                'fields': ('date_of_birth',
                           'date_joined',
                           'last_update',)
                }),
    )

    add_fieldsets = (
            (None, {
                'fields': ('email', 
                           'password', 
                           'username')
            }),
    )

class PersonAdmin(StdUserAdmin):
    model = Person

admin.register(Person, PersonAdmin)
