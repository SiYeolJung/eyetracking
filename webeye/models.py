from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    nickname = models.CharField(max_length=40, blank=True)


class Lecture(models.Model):
    lecture_name = models.CharField(max_length=40)
    teacher = models.CharField(max_length=20)