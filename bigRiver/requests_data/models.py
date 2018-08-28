from django.db import models

# Create your models here.
class requests(models.Model):
    requestID = models.CharField(max_length=10)
    userID = models.CharField(max_length=10)
    date = models.DateField
    type = models.IntegerField
    dealed = models.BooleanField
    dealed1 = models.BooleanField

