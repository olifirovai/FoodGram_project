from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import User, Follow


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    list_display = ('pk', 'username', 'role', 'last_login', 'date_joined',)
    list_filter = ('last_login', 'date_joined',)
    readonly_fields = ['last_login', 'date_joined', ]
    empty_value_display = '-empty-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('user', 'author',)
    list_filter = ('user', 'author',)
    empty_value_display = '-empty-'
