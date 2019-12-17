from django.db import models

from game.models import ExtendUser

"""
獎品
"""
class Prize(models.Model):
    name = models.CharField(max_length=100) # 名稱
    total = models.IntegerField(default=0) # 總數量
    last = models.IntegerField(default=0) # 剩餘
    description = models.CharField(max_length=500) # 獲得資格

    def __str__(self):
        return self.name + '[' + str(self.last) + '/' + str(self.total) + ']'

class OwnPrize(models.Model):
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE) # 獎品
    created_at = models.DateTimeField(auto_now_add=True, editable=False) # 時間
    studentId = models.CharField(max_length=10) # 領獎人

    def __str__(self):
        return self.studentId + '[' + self.prize.name + ']'

class CheckIn(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False) # 時間
    studentId = models.CharField(max_length=10) # 學號

    def __str__(self):
        return self.studentId
