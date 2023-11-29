from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.admin import ModelAdmin


class UserAdmin(ModelAdmin):

    list_display = ['username', 'email', 'first_name', 'last_name']
    list_display_links = ['email']
    readonly_fields = ['id', 'email']
    exclude = ['password']
    


admin.site.register(get_user_model(), UserAdmin)