# -*- coding: utf-8 -*-

# 数据库的测试函数，内容包括增删改查操作的说明。
# 其中，修改操作根据需求的不同，有不同的函数调用，本文件不全部列出。
# 需包含第8-11行代码，若要调用某模型的某类型数据，则import格式如13行。


from __future__ import unicode_literals
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bigRiver.settings")
django.setup()

from basic_info.models import *
from attendance_data.models import *
from request_data.models import *
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

def basic_db_initialize():
    cimodel1 = company_info(companyID='10001', taxNumber='91440300708461136T', bossID='1000001', name='tencent',
                            adminID='1000004@1000005', departNames='Project@Propaganda@HumanResources')
    cimodel2 = company_info(companyID='10002', taxNumber='91110108717743469K', bossID='1000002', name='baidu',
                            adminID='1000006@1000007', departNames='Project@PublicRelations@HumanResources')
    cimodel3 = company_info(companyID='10003', taxNumber='91330100716105852F', bossID='1000003', name='ali',
                            adminID='1000008@1000009', departNames='Technique@Market@HumanResources')

    pimodel1 = personal_info(userID='1000001', password='pwd1', name='Huateng.M', company='10001',
                             departName='Project', modelLocation='1_1', email='htm@qq.com', title=3)
    pimodel2 = personal_info(userID='1000002', password='pwd2', name='Yanhong.L', company='10002',
                             departName='PublicRelations', modelLocation='1_2', email='yhl@qq.com', title=3)
    pimodel3 = personal_info(userID='1000003', password='pwd3', name='Yun.M', company='10003',
                             departName='HumanResources', modelLocation='1_3', email='mayun@qq.com', title=3)

    pimodel4 = personal_info(userID='1000004', password='pwd4', name='jyl', company='10001',
                             departName='Propaganda', modelLocation='1_4', email='jyl@qq.com', title=2)
    pimodel5 = personal_info(userID='1000005', password='pwd5', name='ano', company='10001',
                             departName='HumanResources', modelLocation='1_5', email='ano@qq.com', title=2)
    pimodel6 = personal_info(userID='1000006', password='pwd6', name='lyw', company='10002',
                             departName='Project', modelLocation='1_6', email='lyw@qq.com', title=2)
    pimodel7 = personal_info(userID='1000007', password='pwd7', name='bno', company='10002',
                             departName='HumanResources', modelLocation='1_7', email='htm@qq.com', title=2)
    pimodel8 = personal_info(userID='1000008', password='pwd8', name='lqf', company='10003',
                             departName='Technique', modelLocation='1_8', email='lqf@hotmail.com', title=2)
    pimodel9 = personal_info(userID='1000009', password='pwd9', name='cno', company='10003',
                             departName='Technique', modelLocation='1_9', email='cno@qq.com', title=2)

    pimodel10 = personal_info(userID='1000010', password='pwd10', name='tx1', company='10001',
                             departName='Project', modelLocation='1_10', email='tx1@qq.com', title=1)
    pimodel11 = personal_info(userID='1000011', password='pwd11', name='bd1', company='10002',
                             departName='PublicRelation', modelLocation='2_1', email='bd1@qq.com', title=1)
    pimodel12 = personal_info(userID='1000012', password='pwd12', name='al1', company='10003',
                             departName='Market', modelLocation='2_2', email='htm@qq.com', title=1)
    pimodel13 = personal_info(userID='1000013', password='pwd13', name='tx2', company='10001',
                             departName='Project', modelLocation='2_3', email='tx2@qq.com', title=1)
    pimodel14 = personal_info(userID='1000014', password='pwd14', name='bd2', company='10002',
                             departName='PublicRelation', modelLocation='2_4', email='bd1@qq.com', title=1)
    pimodel15 = personal_info(userID='1000015', password='pwd15', name='al2', company='10003',
                             departName='Market', modelLocation='2_5', email='htm@qq.com', title=1)

    model_list = [cimodel1, cimodel2, cimodel3, pimodel1, pimodel2, pimodel3, pimodel4, pimodel5, pimodel6,
                  pimodel7, pimodel8, pimodel9, pimodel10, pimodel11, pimodel12,pimodel13, pimodel14, pimodel15]
    for model in model_list:
        model.save()



if __name__=="__main__":
    print('yes!')
    # basic_db_initialize()
