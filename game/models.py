from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class ExtendUser(AbstractUser):
    studentId = models.CharField(max_length=8)

"""
問題
"""
class Question(models.Model):
    topic = models.CharField(max_length=10000) # 題目

    created_at = models.DateTimeField(auto_now_add=True, editable=False) # 創建時間
    modified_at = models.DateTimeField(auto_now=True, editable=False) # 修改時間
    is_active = models.BooleanField(default=True) # 是否公開

"""
選項
"""
class Option(models.Model):
    description = models.CharField(max_length=200) # 選項描述
    score = models.IntegerField(default=0) # 選項分數
    question = models.ForeignKey("Question", related_name="choices", on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ("question", "description"), # no duplicated choice per question
        ]

"""
一筆答題記錄
"""
class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    options = models.ManyToManyField("Option") # 選擇的選項

"""
全部答題記錄
"""
class History(models.Model):
    records = models.ManyToManyField("Record") # 選擇的選項
    user = models.OneToOneField("ExtendUser", on_delete=models.CASCADE)
