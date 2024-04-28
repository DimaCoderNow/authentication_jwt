from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(default="", unique=True, max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class RefreshToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField()
    expiration_date = models.DateTimeField()

    class Meta:
        unique_together = (('user', 'token'),)
