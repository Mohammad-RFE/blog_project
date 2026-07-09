from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):

    email = models.EmailField(blank=True)
    profile = models.ImageField(upload_to="profiles/", null=True, blank=True)

    def __str__(self):
        return self.username