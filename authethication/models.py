from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import CustomUserManager
# from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(unique=True)

    # personal
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    # contact
    phone = models.CharField( max_length=17, blank=True, null=True)
    # address
    address_line = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender']

    objects = CustomUserManager()

    def __str__(self):
        return self.email or self.username or str(self.pk)