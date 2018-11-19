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
    cimodel1 = company_info(companyID='10001', taxNumber='91440300708461136T', bossID='1000001', name='腾讯',
                            adminID='1000004@1000005', departNames='项目部@宣传部@人资部')
    cimodel2 = company_info(companyID='10002', taxNumber='91110108717743469K', bossID='1000002', name='百度',
                            adminID='1000006@1000007', departNames='项目部@公关部@人资部')
    cimodel3 = company_info(companyID='10003', taxNumber='91330100716105852F', bossID='1000003', name='阿里',
                            adminID='1000008@1000009', departNames='技术部@市场部@人资部')

    pimodel1 = personal_info(userID='1000001', password='pwd1', name='马化腾', company='10001',
                             departName='项目部', modelLocation='1_1', email='htm@qq.com', title=3)
    pimodel2 = personal_info(userID='1000002', password='pwd2', name='李彦宏', company='10002',
                             departName='公关部', modelLocation='1_2', email='yhl@qq.com', title=3)
    pimodel3 = personal_info(userID='1000003', password='pwd3', name='马云', company='10003',
                             departName='人资部', modelLocation='1_3', email='mayun@qq.com', title=3)

    pimodel4 = personal_info(userID='1000004', password='pwd4', name='江胤霖', company='10001',
                             departName='宣传部', modelLocation='1_4', email='jyl@qq.com', title=2)
    pimodel5 = personal_info(userID='1000005', password='pwd5', name='李煜炜', company='10001',
                             departName='人资部', modelLocation='1_5', email='ano@qq.com', title=2)
    pimodel6 = personal_info(userID='1000006', password='pwd6', name='姜文玉', company='10002',
                             departName='项目部', modelLocation='1_6', email='lyw@qq.com', title=2)
    pimodel7 = personal_info(userID='1000007', password='pwd7', name='张三', company='10002',
                             departName='人资部', modelLocation='1_7', email='htm@qq.com', title=2)
    pimodel8 = personal_info(userID='1000008', password='pwd8', name='李四', company='10003',
                             departName='技术部', modelLocation='1_8', email='lqf@hotmail.com', title=2)
    pimodel9 = personal_info(userID='1000009', password='pwd9', name='王二麻子', company='10003',
                             departName='技术部', modelLocation='1_9', email='cno@qq.com', title=2)

    pimodel10 = personal_info(userID='1000010', password='pwd10', name='刘志', company='10001',
                             departName='项目部', modelLocation='1_10', email='tx1@qq.com', title=1)
    pimodel11 = personal_info(userID='1000011', password='pwd11', name='李米根', company='10002',
                             departName='公关部', modelLocation='2_1', email='bd1@qq.com', title=1)
    pimodel12 = personal_info(userID='1000012', password='pwd12', name='蓝蓝路', company='10003',
                             departName='市场部', modelLocation='2_2', email='htm@qq.com', title=1)
    pimodel13 = personal_info(userID='1000013', password='pwd13', name='葛平', company='10001',
                             departName='项目部', modelLocation='2_3', email='tx2@qq.com', title=1)
    pimodel14 = personal_info(userID='1000014', password='pwd14', name='孙笑川', company='10002',
                             departName='公关部', modelLocation='2_4', email='bd1@qq.com', title=1)
    pimodel15 = personal_info(userID='1000015', password='pwd15', name='本塔特', company='10003',
                             departName='市场部', modelLocation='2_5', email='htm@qq.com', title=1)

    model_list = [cimodel1, cimodel2, cimodel3, pimodel1, pimodel2, pimodel3, pimodel4, pimodel5, pimodel6,
                  pimodel7, pimodel8, pimodel9, pimodel10, pimodel11, pimodel12,pimodel13, pimodel14, pimodel15]
    for model in model_list:
        model.save()

def request_data_initialize():
    rmodel1 = requests(requestID='1', senderID='1000010', receiverID='10001', date='2018-09-10', type=3,
                       content='9月14日：请病假', dealed=0, result=-1, requestdate='9@14')
    rmodel2 = requests(requestID='2', senderID='1000010', receiverID='10001', date='2018-09-10', type=4,
                       content='9月1日：补卡', dealed=0, result=-1, requestdate='9@1')
    rmodel3 = requests(requestID='3', senderID='1000013', receiverID='10001', date='2018-09-10', type=4,
                       content='9月3日：补卡', dealed=0, result=-1, requestdate='9@3')
    rmodel4 = requests(requestID='4', senderID='1000013', receiverID='10001', date='2018-09-10', type=4,
                       content='8月1日：补卡', dealed=0, result=-1, requestdate='8@1')
    rmodel5 = requests(requestID='5', senderID='1000013', receiverID='10001', date='2018-09-10', type=4,
                       content='8月2日：补卡', dealed=0, result=-1, requestdate='8@2')
    rmodel6 = requests(requestID='6', senderID='1000013', receiverID='10001', date='2018-09-10', type=4,
                       content='8月3日：补卡', dealed=0, result=-1, requestdate='8@3')
    rmodel7 = requests(requestID='7', senderID='1000013', receiverID='10001', date='2018-09-10', type=4,
                       content='8月4日：补卡', dealed=0, result=-1, requestdate='8@4')
    rmodel8 = requests(requestID='8', senderID='1000013', receiverID='10001', date='2018-09-10', type=4,
                       content='8月5日：补卡', dealed=0, result=-1, requestdate='8@5')
    rmodel9 = requests(requestID='9', senderID='1000013', receiverID='10001', date='2018-09-10', type=4,
                       content='8月6日：补卡', dealed=0, result=-1, requestdate='8@6')
    rmodel10 = requests(requestID='10', senderID='1000013', receiverID='10001', date='2018-09-10', type=4,
                       content='8月7日：补卡', dealed=0, result=-1, requestdate='8@7')
    model_list = [rmodel1, rmodel2, rmodel3, rmodel4, rmodel5, rmodel6, rmodel7, rmodel8, rmodel9, rmodel10,]
    for m in model_list:
        m.save()


def attendance_data_initialize():
    admodel1 = attendance_data_aug(userID='1000010',
                                   day1='07:40&1@17:02&1',
                                   day2='07:40&1@17:02&1',
                                   day3='07:45&1@17:02&1',
                                   day4='07:45&1@17:02&1',
                                   day5='07:45&1@17:02&1',
                                   day6='07:45&1@17:02&1',
                                   day7='07:450&1@17:02&1',
                                   day8='07:40&1@17:02&1',
                                   day9='07:40&1@17:02&1',
                                   day10='00:00&2@00:00&2',#请假
                                   day11='08:10&0@17:05&1',#迟到
                                   day12='07:42&1@16:30&0',#早退
                                   day13='08:25&0@16:40&0',#迟到早退
                                   day14='07:52&1@17:02&1',
                                   day15='07:52&1@17:02&1',
                                   day16='07:52&1@17:02&1',
                                   day17='07:52&1@17:02&1',
                                   day18='07:52&1@17:13&1',
                                   day19='07:40&1@17:13&1',
                                   day20='07:40&1@17:13&1',
                                   day21='07:40&1@17:13&1',
                                   day22='07:40&1@17:13&1',
                                   day23='07:40&1@17:13&1',
                                   day24='07:40&1@17:13&1',
                                   day25='07:40&1@17:02&1',
                                   day26='07:40&1@17:02&1',
                                   day27='07:40&1@17:02&1',
                                   day28='07:40&1@17:02&1',
                                   day29='07:40&1@17:02&1',
                                   day30='07:40&1@17:02&1',
                                   day31='07:40&1@17:02&1',
                                   )
    admodel2 = attendance_data_aug(userID='1000013',
                                   day1='00:00&2@00:00&2',#请假
                                   day2='07:40&1@17:02&1',
                                   day3='07:45&1@17:02&1',
                                   day4='07:45&1@17:02&1',
                                   day5='07:45&1@17:02&1',
                                   day6='07:45&1@17:02&1',
                                   day7='07:450&1@17:02&1',
                                   day8='07:40&1@17:02&1',
                                   day9='07:40&1@17:02&1',
                                   day10='07:40&1@17:02&1',
                                   day11='07:52&1@17:02&1',
                                   day12='07:42&1@16:30&0',#早退
                                   day13='07:40&1@17:02&1',
                                   day14='07:52&1@17:02&1',
                                   day15='07:52&1@17:02&1',
                                   day16='07:52&1@17:02&1',
                                   day17='07:52&1@17:02&1',
                                   day18='08:10&0@17:05&1',#迟到
                                   day19='07:40&1@17:13&1',
                                   day20='07:40&1@17:13&1',
                                   day21='07:40&1@17:13&1',
                                   day22='07:40&1@17:13&1',
                                   day23='07:40&1@17:13&1',
                                   day24='07:40&1@17:13&1',
                                   day25='07:40&1@17:02&1',
                                   day26='07:40&1@17:02&1',
                                   day27='07:40&1@17:02&1',
                                   day28='07:40&1@17:02&1',
                                   day29='07:40&1@17:02&1',
                                   day30='07:40&1@17:02&1',
                                   day31='08:25&0@16:40&0',#迟到早退
                                   )
    admodel1.save()
    admodel2.save()

if __name__=="__main__":
    print('yes!')
    # attendance_data_initialize()
    # basic_db_initialize()
    request_data_initialize()