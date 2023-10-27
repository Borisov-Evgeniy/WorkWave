from django.contrib import admin
from .models import UserProfile, CustomUser

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'birthday', 'description')
    list_filter = ('user', 'name', 'birthday')
    search_fields = ('user__username', 'name')
    fields = ('user', 'photo_user', 'name', 'birthday', 'description')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(CustomUser)
