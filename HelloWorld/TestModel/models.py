from django.db import models

# Create your models here.

class User(models.Model):       #这里要接受后端需要的，不需要的数据不会关注
    username = models.CharField(
        max_length=20,
        error_messages={'required':"不能为空"})  #表单中的name要与变量名一样
    password = models.CharField(
        max_length=20,
        error_messages={'required':"不能为空",
                        'min_length':'密码长度不小于5',},)
