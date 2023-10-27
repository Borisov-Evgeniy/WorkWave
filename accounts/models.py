from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_executor = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, verbose_name=("groups"), blank=True, related_name='customuser_groups')
    user_permissions = models.ManyToManyField(Permission, verbose_name=("user permissions"),blank=True,related_name='customuser_user_permissions')

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    photo_user = models.ImageField()
    name = models.CharField(max_length=100, null=True, blank=True)
    birhday = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return self.name