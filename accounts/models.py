from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_executor = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    photo_user = models.ImageField()
    name = models.CharField(max_length=100, null=True, blank=True)
    birhday = models.DateTimeField(auto_now_add=True)
    description = models.TextField()