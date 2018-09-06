# -*- coding: utf-8 -*-

# 数据库的测试函数，内容包括增删改查操作的说明。
# 其中，修改操作根据需求的不同，有不同的函数调用，本文件不全部列出。
# 需包含第8-11行代码，若要调用某模型的某类型数据，则import格式如13行。


from __future__ import unicode_literals
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bigRiver.settings")
django.setup()

from basic_info.models import personal_info
from attendance_data.models import *

#插入一条数据
def insert_demo(id, pwd):
    temp_personal_info = personal_info(userID=id, password=pwd)
    temp_personal_info.save()
    return True

#查询数据
def select_demo():
    #现在已插入插入两条数据，分别为(1000001, pwd)和(1000002, pwd)

    #获取整个数据集
    entire_model = personal_info.objects.all()

    print(entire_model[0].userID)
    #输出的是第一条数据的userID,即为100001

    #条件查询
        #该查询方式仅限查询对象恰为1个的情况，否则报错，可在get函数具体实现方法中查看
    searching_model1 = personal_info.objects.get(userID='1000001')
    print(searching_model1.password)
    #searching_model1是userID='1000001'的行，输出为pwd

        #该查询方式取一整列
    searching_model2 = personal_info.objects.all().values('userID')
    print(searching_model2)

        #该查询方式相当于select * from table where password = 'pwd'
    searching_model3 = personal_info.objects.filter(password='pwd')
    print(searching_model3)

        #该查询方式相当于select * from table where password != 'pwd'
    searching_model4 = personal_info.objects.exclude(password='pwd')
    print(searching_model4)

#修改某条数据
def update_demo():
    #步骤1：先调出待修改数据，此处查询第1条
    searching_model1 = personal_info.objects.get(userID='1000001')
    #步骤2：更改该条数据
    searching_model1.name = "liyuwang"
    #步骤3：将该条数据重新存入(修改编码方式前存中文会报错)
    searching_model1.save()
    #p.s.：调出该模型进行查看
    searching_model2 = personal_info.objects.get(userID='1000001')
    print(searching_model2.name)

#删除一条数据
def delete_demo():
    #先插入一条数据
    if(insert_demo('1000003', 'pwd3')):
        the_model = personal_info.objects.get(userID='1000003')
        print(the_model.password)
        the_model.delete()


if __name__=="__main__":
    delete_demo()