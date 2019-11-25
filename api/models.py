from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.

class ExtendUser(AbstractUser):
    studentId = models.CharField(max_length=8)
    nickName = models.CharField(max_length=6)
    score = models.IntegerField(default=0)

class Question(models.Model):
    topic = models.CharField(max_length=10000)
    correctOption = ArrayField(models.CharField(max_length=10000), size=4)
    wrongOption = ArrayField(models.CharField(max_length=10000), size=4)