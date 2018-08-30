import os, django
import sys
import basic_info
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bigRiver.settings")
django.setup()

#个人信息管理模块

from basic_info.models import *

def dbtest():
    temp_personal_info = personal_info(userID='1000004', email='temp')
    temp_personal_info.save()
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
    elif(select_result.password != password):
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


def modify():
    #userID不改变，request中放置状态码、用户名和更改后的内容。
    #1：password 2：name 3：company 4：mail 5：modelLocation
    return True

def modify_info():
    return True

def create_company():
    return True


if(__name__ == "__main__"):
    dbtest()