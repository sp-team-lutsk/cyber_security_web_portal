from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import StdUser

class StdUserAdmin(UserAdmin):
    model = StdUser

    list_display = ('email', 'username', 'is_staff', 'is_active',)
    list_filter = ('email',)
    readonly_fields = ('date_joined', 'is_staff', 'is_active', 'is_admin')

admin.site.register(StdUser, StdUserAdmin)
