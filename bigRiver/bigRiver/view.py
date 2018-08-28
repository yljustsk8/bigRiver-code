from django.shortcuts import render,HttpResponse,redirect,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django import forms

#表单
class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())


def login(request):
    if request.method=="GET":
        return render(request,'login.html')
    if request.method=='POST':
        uf=UserForm(request.POST)
        # if uf.is_valid():
            # 获取表单用户密码
            # username = uf.cleaned_data['username']
            # password = uf.cleaned_data['password']
            # 获取的表单数据与数据库进行比较
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

def calendar(request):
    return render_to_response('calendar.html')


def face(request):
    return render_to_response('face.html')
