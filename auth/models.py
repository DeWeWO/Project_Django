from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=255)
    phone_number = PhoneNumberField(unique=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"]
    
    objects = UserManager()
    
    def __str__(self):
        return self.email

