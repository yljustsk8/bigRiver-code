from django.db import models

# Create your models here.

class personal_info(models.Model):
    userID = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    name = models.CharField(max_length=10)
    company = models.CharField(max_length=20)
    departName = models.CharField(max_length=10)
    modelLocation = models.CharField(max_length=10)

class company_info(models.Model):
    companyID = models.CharField(max_length=20)
    taxNumber = models.CharField(max_length=20)
    bossID = models.CharField(max_length=10)
    adminID = models.CharField(max_length=10)
    departNames = models.CharField(max_length=10)
