import os, django
import sys
import basic_info
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bigRiver.settings")
django.setup()

#个人信息管理模块

from basic_info.models import *

def dbtest():
    userID = '1000001'
    company = 'dajiang'
    taxNumber = '91350505577034942J'



def login(request):
    #提取输入的userID和password
    userID = request.POST['userID']
    password = request.POST['password']
    #在数据库中找出userID匹配项
    select_result = personal_info.objects.filter(userID=userID)
    if not select_result:
        #id不存在
        print("id doesn't exist!")
    elif(select_result[0].password != password):
        #密码错误
        print("wrong password!")
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

    return True


if(__name__ == "__main__"):
    dbtest()