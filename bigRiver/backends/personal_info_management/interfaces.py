import os, django
import sys
import basic_info
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bigRiver.settings")
django.setup()

#个人信息管理模块

from basic_info.models import *

def dbtest():
    return True

def login(request):
    #提取输入的userID和password
    userID = request.POST['userID']
    password = request.POST['password']
    #在数据库中找出userID匹配项
    select_result = personal_info.objects.filter(userID=userID)
    if not select_result:
        #id不存在
        print("id doesn't exist!")
        return False
    elif(select_result[0].password != password):
        #密码错误
        print("wrong password!")
        return False
    else:
        return True

def register(request):
    #提取信息
    userID = request.POST['userID']
    password = request.POST['password']
    check_id_result = personal_info.objects.filter(userID=userID)
    if check_id_result:
        #id已存在
        print("id existed!")
    else:
        #注册成功
        the_model = personal_info(userID=userID, password=password)
        the_model.save()
        print("register success!")
        return True
    return True

def modify(request):
    #userID不改变，request中放置状态码、用户名和更改后的内容。
    #1：password 2：name 3：mail
    status = request.POST['status']
    userID = request.POST['userID']
    info = request.POST['info']#此处'info'内容待定
    if not modify_info(status, userID, info):
        print("id doesn't exist")
    else:
        print("change success")
    return True

def modify_info(status, userID, info):
    #userID不改变，request中放置状态码、用户名和更改后的内容。
    #1：password 2：name 3：email 4：company 5：departmentName 6：modelLocation
    select_result = personal_info.objects.filter(userID=userID)
    if not select_result:
        print("id doesn't exist!")
        return Flase
    the_model=select_result[0]
    if(status==1):
        the_model.password=info
    elif(status==2):
        the_model.name=info
    elif(status==3):
        the_model.email=info
    elif(status==4):
        the_model.company=info
    elif(status==5):
        the_model.departName=info
    elif(status==6):
        the_model.modelLocation=info
    the_model.save()

    test_string = str(status)
    print('turn info '+test_string+' to '+ info)
    return True

def create_company(request):
    userID = request.POST['userID']
    company_name = request.POST['companyName']
    taxNumber = request.POST['taxNumber']

    # 当前companyID自增，获取新的companyID
    entire_model = company_info.objects.all()
    l = len(entire_model)
    new_company_id = int(entire_model[l - 1].companyID) + 1
    new_model = company_info(companyID=new_company_id, bossID=userID, name=company_name, taxNumber=taxNumber)
    new_model.save()
    #按照逻辑，税号和公司名需要进行判断，此处暂未进行编写
    return True

if(__name__ == "__main__"):
    dbtest()