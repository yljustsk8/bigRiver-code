from django.shortcuts import render,HttpResponse,redirect,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from backends.personal_info_management import interfaces as pim
from backends.company_management import interfaces as cm
from backends.attendance_checking import interfaces as ac
import json
import base64
import os
import datetime

from backends.ai.face_model import save_face
#表单
class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())



def login(request):
    if request.method=="GET":
        return render(request,'login.html')
    if request.method=='POST':
        if(pim.login(request)):
            request.set_cookie('user_id', request.POST.get('userID'), 3600)
            response = HttpResponseRedirect('../user/')
            return response





def regist(request):
    uf = UserForm(request.POST)
    if uf.is_valid():
        # 获取表单用户密码
        username = uf.cleaned_data['username1']
        password = uf.cleaned_data['password1']
        password2 = request.POST.get('password2')

        # user = User.objects.filter(username__exact=username)
        # if user:
        #     不能重名
            # return render(request, 'login.html')
            # 将username写入浏览器cookie,失效时间为3600
            # return HttpResponse("<p>不能重名！</p>")
        # else:
        #     用户名独立，比较密码是否重复
            # if password==password2:
            # 存入数据库
            #     reg = User(username=username, password=password)
            #     reg.save()
            #     return render(request, 'login.html')
            #     return HttpResponse("<p>注册成功!</p>")
            # else:
            #     return HttpResponse("<p>两次输入密码不符！</p>")

        # 将username写入浏览器cookie,失效时间为3600
        # response.set_cookie('username', username, 3600)
        # return response


def user(request):
    if request.method == "GET":
        return render_to_response('user.html')
    if request.method == "POST":
        month=request.POST.get('content')
        user_id=request.POST.get('user_id')
        # result=ac.view_single_calendar(month, user_id)
        return HttpResponse(json.dumps("result"), content_type="application/json")

def calendar(request):
    if request.method == "GET":
        return render_to_response('calendar.html')


def face(request):
    return render_to_response('face.html')

def upload_image(request):
    data = {'success': 0}
    if request.method=="POST":
        img = ""
        name = ""
        if 'image' in request.POST:
            img = request.POST['image'].split(',')[1]
        if 'name' in request.POST:
            name = request.POST['name']
        if name=="":
            name="temp.jpg"
        if img != "":
            img = base64.b64decode(img)
            cur = os.path.abspath(".")
            save_path = os.path.join(cur, "bigRiver\\static\\images\\" + name)
            with open(save_path, "wb") as file:
                file.write(img)
            data['success'] = 1
    elif request.method=="GET":
        img=""
        name="temp.jpg"
        if 'image' in request.GET:
            img=request.GET['image'].split(',')[1]
        if 'name' in request.GET:
            name=request.GET['name']
        if img!="":
            img=base64.b64decode(img)
            cur=os.path.abspath(".")
            save_path=os.path.join(cur,"bigRiver\\static\\images\\"+name)
            with open(save_path, "wb") as file:
                file.write(img)
            data['success']=1
    return HttpResponse(json.dumps(data),content_type="application/json")

def admin_employees(request):
    user_table = {
        'count': 10,
        'info': [
            {
                'user_id': "250",
                'name': "lyw",
                'dpmt': "qianduan",
                'time_in': "05:00",
                'time_out': "20:00",
                'status': "早退"
            },
            {
                'user_id': "251",
                'name': "lqf",
                'dpmt': "qianduan",
                'time_in': "06:00",
                'time_out': "21:00",
                'status': "迟到"
            }
        ]
    }

    if request.method=="GET":
        print("GET ", request.GET.get('content'))
        if request.GET.get('content') == None:
            return render(request, 'admin_employees.html')
        elif request.GET.get('content')=='requests':
            response = HttpResponseRedirect('/requests/')
            return response

    if request.method=='POST':
        print("POST ",request.POST.get('content'))
        return HttpResponse(json.dumps(user_table), content_type="application/json")

def admin_requests(request):

    user_table2 = {
        'count': 10,
        'info': [
            {
                'request_id': "1",
                'user_id': "250",
                'name': "lyw",
                'dpmt': "qianduan",
                'type': "请病假"
            },
            {
                'request_id': "2",
                'user_id': "255",
                'name': "lqf",
                'dpmt': "qianduan",
                'type': "请病假"
            },
            {
                'request_id': "3",
                'user_id': "260",
                'name': "jyl",
                'dpmt': "qianduan",
                'type': "请病假"
            }
        ]
    }

    if request.method=="GET":
        print("GET ", request.GET.get('content'))
        if request.GET.get('content') == None:
            return render(request, 'admin_requests.html')
        elif request.GET.get('content')=='employees':
            response = HttpResponseRedirect('../admin/')
            return response
    if request.method=='POST':
        if request.POST.get('content') == 'show requests':
            return HttpResponse(json.dumps(user_table2), content_type="application/json")

def boss_admins(request):
    user_table = {
        'count': 10,
        'info': [
            {
                'user_id': "250",
                'name': "lyw",
                'dpmt': "qianduan",
                'status': "早退",
                'title': "普通员工"
            },
            {
                'user_id': "251",
                'name': "lqf",
                'dpmt': "qianduan",
                'status': "迟到",
                'title': "管理员"
            }
        ]
    }
    if request.method=="GET":
        print("GET ", request.GET.get('content'))
        if request.GET.get('content') == None:
            return render(request, 'boss_admins.html')
        elif request.GET.get('content')=='not_boss':
            response = HttpResponseRedirect('../admin/')
            return response
    if request.method=='POST':
        print("POST ", request.POST.get('content'))
        if request.POST.get('content') == 'show admins':
            return HttpResponse(json.dumps(user_table), content_type="application/json")
        elif request.POST.get('content') == 'delete admin':
            result=cm.delete_admin(pim.get_company_ID(request.GET.get('enforcer')), request.GET.get('employee'))
            return result
        elif request.POST.get('content') == 'add admin':
            result=cm.set_admin(pim.get_company_ID(request.GET.get('enforcer')), request.GET.get('employee'))
            return result


def boss_requests(request):
    user_table2 = {
        'count': 10,
        'info': [
            {
                'request_id': "1",
                'user_id': "250",
                'name': "lyw",
                'dpmt': "qianduan",
                'type': "请病假"
            },
            {
                'request_id': "2",
                'user_id': "255",
                'name': "lqf",
                'dpmt': "qianduan",
                'type': "请病假"
            },
            {
                'request_id': "3",
                'user_id': "260",
                'name': "jyl",
                'dpmt': "qianduan",
                'type': "请病假"
            }
        ]
    }

    if request.method=="GET":
        print("GET ", request.GET.get('content'))
        if request.GET.get('content') == None:
            return render(request, 'boss_requests.html')
        elif request.GET.get('content')=='not_boss':
            response = HttpResponseRedirect('../admin/')
            return response
    if request.method=='POST':
        if request.POST.get('content') == 'show requests':
            return HttpResponse(json.dumps(user_table2), content_type="application/json")
