from django.db import models

# Create your models here.

class personal_info(models.Model):
    userID = models.CharField(max_length=10, default='')
    password = models.CharField(max_length=20, default='')
    email = models.CharField(max_length=50, default='')
    name = models.CharField(max_length=10, default='')
    company = models.CharField(max_length=20, default='')
    departName = models.CharField(max_length=50, default='')
    # 0=user;1=stuff;2=administrator;3=boss
    title = models.IntegerField(default=0)
    modelLocation = models.CharField(max_length=10, default='')

class company_info(models.Model):
    companyID = models.CharField(max_length=20, default='')
    name = models.CharField(max_length=20, default='')
    taxNumber = models.CharField(max_length=20, default='')
    bossID = models.CharField(max_length=10, default='')
    adminID = models.CharField(max_length=100, default='')
    departNames = models.CharField(max_length=500, default='')
