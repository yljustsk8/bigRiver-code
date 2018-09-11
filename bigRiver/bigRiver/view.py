from django.shortcuts import render,HttpResponse,redirect,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from backends.personal_info_management import interfaces as pim
from backends.company_management import interfaces as cm
from backends.attendance_checking import interfaces as ac
from backends.mail_management import interfaces as mm
from backends.ai import face_model
import json
import base64
import os
import shutil
import time
#表单
class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())



def login(request):
    if request.method=="GET":
        return render(request,'login.html')
    if request.method=='POST':
        result = pim.login(request.POST.get('user_id'),request.POST.get('password'))
        if result['status']:
            titles = ('user','user','admin','boss')
            response = HttpResponseRedirect('../'+titles[result['title']]+'/')
            response.set_cookie('user_id', request.POST.get('user_id'))
            return response
        else:
            return HttpResponse(result['content'])


def regist(request):
    if request.method== "GET":
        return render_to_response("login.html");
    if request.method=="POST":
        user_id = request.POST.get('userID_signUp')
        password = request.POST.get('password_signUp')
        name = request.POST.get('name_signUp')
        email = request.POST.get('email_signUp')
        result = pim.register(user_id, password, name, email)
        if result['status']:
            return HttpResponse(result['content'])
        else:
            return HttpResponse(False)

def user(request):
    return render_to_response("user.html");


def user_company(request):
    if request.method == "GET":
        return render_to_response('join_company.html')
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        result = pim.get_company_ID(user_id)
        if result != False:
            return HttpResponse(result)
        else:
            return HttpResponse(False)

def search_company(request):
    #result = cm.get_cominfo_by_id(request.POST.get('company_id'))
    result = "BOT"
    if result!=False:
        return HttpResponse(result)
    else:
        return HttpResponse(False)


def confirm_join(request):
    user_id = request.POST.get('user_id')
    company_id = request.POST.get('company_id')
    status = request.POST.get('status')
    if status:
        result = pim.join_company(user_id, company_id)
        if result != False:
            return HttpResponse(True)
        else:
            return HttpResponse(False)
    else:
        return HttpResponse(False)

def create_company(request):
    if request.method == 'GET':
        return render_to_response("create_company.html")
    if request.method == 'POST':
        user_id = request.POST.get('user_id_create')
        company_name = request.POST.get('name_create')
        taxNumber_create = request.POST.get('taxNumber_create')
        print(user_id+" "+company_name +" "+taxNumber_create)
        result = pim.create_company(user_id, company_name, taxNumber_create)
        return HttpResponse(json.dumps(result), content_type="application/json")




def user_edit(request):
    user_id = request.POST.get('user_id')
    name = request.POST.get('name')
    password =request.POST.get('password')
    email = request.POST.get('email')
    print(user_id)
    print(name)
    name_edit = True; password_edit = True; email_edit = True;
    if name != '':
        name_edit = pim.modify(user_id, 2, name)['status']
    if password != '':
        password_edit = pim.modify(user_id, 1, password)['status']
    if email != '':
        email_edit = pim.modify(user_id, 3, email)['status']
    if name_edit and password_edit and email_edit:
        result = True
    else:
        result = False
    return HttpResponse(result)


def user_info(request):
    user_id = request.POST.get('user_id')
    result_dict = pim.get_info_by_id(user_id)
    result = {'name': result_dict['name'],
              'email': result_dict['email'],
              'password':result_dict['password'],}
    return HttpResponse(json.dumps(result), content_type="application/json")


def about_us(request):
    return render_to_response("BOT.html")

def calendar(request):
    if request.method == "GET":
        return render_to_response('calendar.html')
    if request.method == "POST":
        user_id=request.POST.get('user_id')
        result=ac.view_single_year_calendar(user_id)
        return HttpResponse(json.dumps(result), content_type="application/json")


def face(request):
    return render_to_response('face.html')

def upload_image(request):
    data = {'success': 0}
    if request.method=="POST":
        img = ""
        name = ""
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
def face_camera(request):
    return render_to_response("camera.html")

def face_enter(request):
    data = {'success': 0}

    temp_save_path = "bigRiver/static/temp"
    if not os.path.exists(temp_save_path):
        os.makedirs(temp_save_path)

    if request.method=="GET":
        userID=""
        stop=""
        if not 'stop' in request.GET or not 'user_id' in request.GET:
            return HttpResponse(json.dumps(data), content_type="application/json")
        stop=request.GET['stop']
        userID=request.GET['user_id']

        save_path = os.path.join(temp_save_path, userID)
        if not os.path.exists(save_path):
            return HttpResponse(json.dumps(data), content_type="application/json")
        success=face_model.face_enter_url(userID,save_path)
        data['success']=success
        shutil.rmtree(save_path)

    if request.method=="POST":
        userID=""
        img=""

        if not 'user_id' in request.POST or not 'image' in request.POST:
            return HttpResponse(json.dumps(data), content_type="application/json")
        userID=request.POST['user_id']

        save_path = os.path.join(temp_save_path, userID)
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        img_num=len(os.listdir(save_path))
        img_save_path=os.path.join(save_path,"{}.jpg".format(img_num+1))


        img = request.POST['image'].split(',')[1]
        img=base64.b64decode(img)
        with open(img_save_path,'wb') as file:
            file.write(img)
        useful=face_model.is_useful(img_save_path)
        print(useful)
        if useful:
            data['success']=1
        else:
            if os.path.exists(save_path):
                os.remove(img_save_path)
    return HttpResponse(json.dumps(data), content_type="application/json")

def admin_employees(request):
    # user_table = {
    #     'count': 10,
    #     'info': [
    #         {
    #             'user_id': "250",
    #             'name': "lyw",
    #             'dpmt': "qianduan",
    #             'time_in': "05:00",
    #             'time_out': "20:00",
    #             'status': "早退"
    #         },
    #         {
    #             'user_id': "251",
    #             'name': "lqf",
    #             'dpmt': "qianduan",
    #             'time_in': "06:00",
    #             'time_out': "21:00",
    #             'status': "迟到"
    #         }
    #     ]
    # }

    if request.method=="GET":
        print("GET ", request.GET.get('user_id'))
        if request.GET.get('content') == None:
            return render(request, 'admin_employees.html')
        elif request.GET.get('content')=='requests':
            response = HttpResponseRedirect('/requests/')
            return response

    if request.method=='POST':
        print("POST ", request.POST.get('content'))
        if request.POST.get('content') == 'show employees':
            user_table = ac.view_all_calendar(time.strftime('%m'), time.strftime('%d'), request.POST.get('user_id'))
            return HttpResponse(json.dumps(user_table), content_type="application/json")

def admin_requests(request):
    if request.method=="GET":
        print("GET ", request.GET.get('content'))
        if request.GET.get('content') == None:
            return render(request, 'admin_requests.html')
    if request.method=='POST':
        if request.POST.get('content') == 'show requests':
            print(request.POST.get('user_id'))
            user_table=mm.get_request(request.POST.get('user_id'))
            return HttpResponse(json.dumps(user_table), content_type="application/json")

def boss_admins(request):
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
            user_table=ac.view_all_calendar(time.strftime('%m'),time.strftime('%d'),request.POST.get('user_id'))
            return HttpResponse(json.dumps(user_table), content_type="application/json")
        elif request.POST.get('content') == 'delete admin':
            result=cm.delete_admin(pim.get_company_ID(request.POST.get('enforcer')), request.POST.get('employee'))
            return result
        elif request.POST.get('content') == 'add admin':
            result=cm.set_admin(pim.get_company_ID(request.POST.get('enforcer')), request.POST.get('employee'))
            return result


def boss_requests(request):
    if request.method=="GET":
        print("GET ", request.GET.get('content'))
        if request.GET.get('content') == None:
            return render(request, 'boss_requests.html')
    if request.method=='POST':
        if request.POST.get('content') == 'show requests':
            user_table=mm.get_request(request.POST.get('user_id'))
            return HttpResponse(json.dumps(user_table), content_type="application/json")

def handle_requests(request):
    # 申请加入   type=1  senderID = userID  receiverID = companyID
    # 邀请加入   type=2  senderID = companyID  receiverID = userID
    # 申请请假   type=3  senderID = userID  receiverID = companyID
    # 申请补卡   type=4  senderID = userID  receiverID = companyID
    if request.method == 'POST':
        request_id=request.POST.get('request_id')
        type=request.POST.get('type')
        result_str=request.POST.get('result')
        result=(result_str=='1')
        print('handle_request: '+request_id+'  '+type+'  '+result_str)
        if type=='1':
            confirm_code=mm.answer_join(request_id,result)
        else:
            confirm_code=mm.answer_other_req(request_id, result)
        if confirm_code:
            confirm_data='修改成功'
        else:
            confirm_data = '修改失败，请稍后重试'
        return HttpResponse(json.dumps(confirm_data), content_type="application/json")

def send_requests(request):
    if request.method =='GET':
        return render_to_response('calendar_request.html')
    if request.method == 'POST':
        sender_id=request.POST.get('user_id')
        type=request.POST.get('request_type')
        content=request.POST.get('request_content')
        month=request.POST.get('month')
        date=request.POST.get('date')
        if type:
            confirm_code=mm.send_request(sender_id,month,date,3,content)
        else:
            confirm_code = mm.send_request(sender_id, month, date, 4, content)
        if confirm_code:
            confirm_data='申请成功'
        else:
            confirm_data = '申请失败，请稍后重试'
        return HttpResponse(json.dumps(confirm_data), content_type="application/json")

