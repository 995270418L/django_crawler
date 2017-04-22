from django.db import models
from django.utils import timezone

# Create your models here.

#Cookie 保存cookie两个月更新一次
class Cookies(models.Model):
    ds_user_id = models.CharField(max_length=225)
    sessionid = models.CharField(max_length=225)
    save_date = models.DateTimeField('save date')
    expire_date = models.DateTimeField('expire date')

    def __str__(self):
        return str(self.ds_user_id) + str(self.sessionid)

#Message 用户留言反馈
class Message(models.Model):
    username = models.CharField(max_length=30)
    message = models.TextField
    ip = models.CharField(max_length=32)

    def __str__(self):
        return self.username + self.message

# Visitor  用户访问记录
class Visitor(models.Model):
    ip = models.CharField(max_length=32)
    visitor_date = models.DateTimeField(auto_now=True)