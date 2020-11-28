from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'role', 'last_login', 'date_joined',)
    list_filter = ('last_login', 'date_joined',)
    readonly_fields = ['last_login', 'date_joined', ]
    empty_value_display = '-empty-'
