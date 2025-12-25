from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    profile_picture=models.ImageField(upload_to='profile_picture/')

    class Meta:
        db_table='inventory_user'
