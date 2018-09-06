from django.db import models

#申请加入   type=1  senderID = userID  receiverID = companyID
#邀请加入   type=2  senderID = companyID  receiverID = userID
#申请请假   type=3  senderID = userID  receiverID = companyID
#申请补卡   type=4  senderID = userID  receiverID = companyID

# Create your models here.
class requests(models.Model):
    requestID = models.CharField(max_length=10, default='')
    senderID = models.CharField(max_length=10, default='')
    receiverID = models.CharField(max_length=10, default='')
    date = models.CharField(max_length=10, default='')
    type = models.IntegerField(default=-1)
    content = models.CharField(max_length=100, default='')
    dealed = models.BooleanField(default=False)
    #如果同意，则为1，如果是不同意，则为0
    result = models.IntegerField(default=-1)
    requestdate = models.CharField(max_length=10, default='')