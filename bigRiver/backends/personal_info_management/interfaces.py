import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bigRiver.settings")
django.setup()

#个人信息管理模块

from basic_info.models import *
from bigRiver.view import UserForm


def login(request):
    uf = UserForm(request.POST())
    if uf.is_valid():
        # 获取表单用户密码
        userID = uf.cleaned_data['username']
        password = uf.cleaned_data['password']
        model = personal_info.objects.get(userID=userID)
        if(model.password==password):
            print(userID + " in pim.interfaces.login success!")
            return True
        return False

def register():
    return True


def modify():
    return True


def create_company():
    return True


if(__name__ == "__main__"):
    login("1000001", "pwd");