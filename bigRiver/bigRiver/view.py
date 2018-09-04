from django.shortcuts import render,HttpResponse,redirect,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from backends.personal_info_management import interfaces as pim
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
            response = HttpResponseRedirect('../index/')
            return response


            # user = User.objects.filter(username__exact=username, password__exact=password)
            # if user:
                # 比较成功，跳转index
                # response = HttpResponseRedirect('../index/')
                # 将username写入浏览器cookie,失效时间为3600
                # response.set_cookie('username', username, 3600)
                # return response
            # else:
                # 比较失败，还在login
                # return render(request, 'login.html')
        # else:
        #     return render(request,'login.html',{'uf':uf})

#登陆成功
def index(request):
    username = request.COOKIES.get('username','')
    return render_to_response('index.html' ,{'username':username})

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

def calendar1(request):
    return render_to_response('calendar1.html')


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

def admin(request):
    if request.method=="GET":
        return render(request,'admin.html')
    if request.method=='POST':
        # time=datetime.datetime.now().strftime('%Y-%m-%d')
        # userID=request.GET.get('userID')
        # ac.view_all_calendar(time,userID)

        user_table={
            'count':10,
            'info':[
                {
                    'id':"250",
                    'name':"lyw",
                    'dpmt':"qianduan",
                    'time_in':"05:00",
                    'time_out':"20:00",
                    'status':"早退"
                },
                {
                    'id': "251",
                    'name': "lqf",
                    'dpmt': "qianduan",
                    'time_in': "06:00",
                    'time_out': "21:00",
                    'status': "迟到"
                }
            ]
        }
        return HttpResponse(json.dumps(user_table),content_type="application/json")