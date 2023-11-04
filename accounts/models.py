from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission, Group
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(username, email, password, **extra_fields)
class CustomUser(AbstractUser):
    CUSTOMER = 'customer'
    EXECUTOR = 'executor'
    ROLE_CHOICES = (
        (CUSTOMER, 'Заказчик'),
        (EXECUTOR, 'Исполнитель'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=CUSTOMER)
    photo_user = models.ImageField(upload_to='user_photos/', null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(Group, verbose_name=("groups"), blank=True, related_name='customuser_groups')
    user_permissions = models.ManyToManyField(Permission, verbose_name=("user permissions"), blank=True,
                                              related_name='customuser_user_permissions')

objects = CustomUserManager()