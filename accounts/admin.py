from django.contrib import admin
from .models import CustomUser

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'birthday', 'description')
    list_filter = ('user', 'name', 'birthday')
    search_fields = ('user__username', 'name')
    fields = ('user', 'photo_user', 'name', 'birthday', 'description')

admin.site.register(CustomUser)
