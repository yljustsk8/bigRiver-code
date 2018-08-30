import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bigRiver.settings")
django.setup()

#个人信息管理模块

from basic_info.models import *


def login(request):
    return True

def register():
    return True


def modify():
    return True


def create_company():
    return True


if(__name__ == "__main__"):
    login("1000001", "pwd");