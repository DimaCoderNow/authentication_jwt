from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    '''
    User Model:

    Fields:
        - password: CharField
        - first_name: CharField
        - last_name: CharField
        - is_staff: BooleanField
        - is_active: BooleanField
        - is_superuser: BooleanField
        - date_joined: DateTimeField

    Additional Fields:
        - email: EmailField
        - username: CharField
    '''
    email = models.EmailField(unique=True)
    username = models.CharField(default="", unique=True, max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class RefreshToken(models.Model):
    '''
    RefreshToken Model:

    Fields:
        - user: ForeignKey to User
        - token: UUIDField
        - expiration_date: DateTimeField
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField()
    expiration_date = models.DateTimeField()

    class Meta:
        unique_together = (('user', 'token'),)
