from django.contrib.auth.models import AbstractUser
from django.db import models

"""
問題
"""
class Question(models.Model):
    topic = models.CharField(max_length=10000) # 題目
    solution = models.CharField(max_length=1000) # 詳解
    option_1 = models.CharField(max_length=200) # 選項描述
    option_2 = models.CharField(max_length=200) # 選項描述
    option_3 = models.CharField(max_length=200) # 選項描述
    option_4 = models.CharField(max_length=200) # 選項描述
    correct_option = models.CharField(max_length=200) # 選項描述

    def __str__(self):
        return self.topic

"""
一題記錄
"""
class Round(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) #回答的問題
    select_option = models.CharField(max_length=200, blank=True) #選擇的選項

"""
一回合答題記錄
"""
class History(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    record = models.ManyToManyField(Round)
    score = models.IntegerField(default=0) # 分數

class ExtendUser(AbstractUser):
    studentId = models.CharField(max_length=10, unique=True) #學號
    history = models.ManyToManyField(History)
