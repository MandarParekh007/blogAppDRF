from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from .managers import CustomUserManager

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address must be there'), unique=True)
    bio = models.CharField(max_length=100)
    picture = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    username = models.CharField(max_length=50, unique=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username','phone')

    objects = CustomUserManager()

    def __str__(self):
        return self.email