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
import shutil

#表单
class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())



def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == 'POST':
        result = pim.login(request.POST.get('user_id'), request.POST.get('password'))
        return HttpResponse(json.dumps(result), content_type="application/json")
    # if request.method=="GET":
    #     return render(request,'login.html')
    # if request.method=='POST':
    #     result = pim.login(request.POST.get('user_id'),request.POST.get('password'))
    #     if result['status']:
    #         titles = ('user','user','admin','boss')
    #         response = HttpResponseRedirect('../'+titles[result['title']]+'/')
    #         response.set_cookie('user_id', request.POST.get('user_id'))
    #         return response
    #     else:
    #         return HttpResponse(result['content'])


def regist(request):
    # if request.method== "GET":
    #     return render_to_response("login.html");
    # if request.method=="POST":
    #     user_id = request.POST.get('userID_signUp')
    #     password = request.POST.get('password_signUp')
    #     name = request.POST.get('name_signUp')
    #     email = request.POST.get('email_signUp')
    #     result = pim.register(user_id, password, name, email)
    #     if result['status']:
    #         return HttpResponse(result['content'])
    #     else:
    #         return HttpResponse(False)
    if request.method == "GET":
        return render_to_response("login.html");
    if request.method == "POST":
        user_id = request.POST.get('userID_signUp')
        password = request.POST.get('password_signUp')
        name = request.POST.get('name_signUp')
        email = request.POST.get('email_signUp')
        result = pim.register(user_id, password, name, email)
        return HttpResponse(json.dumps(result), content_type="application/json")


def user(request):
    return render_to_response("user.html");


def user_company(request):
    if request.method == "GET":
        return render_to_response('join_company.html')
    if request.method == "POST":
        cominfo_dict = {
            'success':0,
            'companyID': '',
            'taxNumber': '',
            'bossID': '',
            'adminID': '',
            'departNames': '',
            'name': ''
        }
        user_id = request.POST.get('user_id')
        result = pim.get_company_ID(userID=user_id)
        if(result.strip() != ''):
            cominfo = cm.get_cominfo_by_id(result)
            if not cominfo is None:
                cominfo_dict=cominfo
                cominfo_dict['success']=1
        return HttpResponse(json.dumps(cominfo_dict), content_type="application/json")

def identify(request):
    data = {'success': 0}
    temp_identify_path="bigRiver/static/temp/identify"
    if not os.path.exists(temp_identify_path):
        os.makedirs(temp_identify_path)
    temp_file_num=len(os.listdir(temp_identify_path))
    img_save_path=os.path.join(temp_identify_path,"temp_{}".format(temp_file_num))
    if not os.path.exists(img_save_path):
        os.makedirs(img_save_path)
    imgs=[]
    img_urls=[]
    if request.method=="POST":
        if  not 'image1' in request.POST and not 'image2' in request.POST and not 'image3' in request.POST:
            return HttpResponse(json.dumps(data), content_type="application/json")
        imgs.append(base64.b64decode(request.POST['image1'].split(',')[1]))
        imgs.append( base64.b64decode(request.POST['image2'].split(',')[1]))
        imgs.append( base64.b64decode(request.POST['image3'].split(',')[1]))
        for i in range(3):
            img_url="{}.jpg".format(i)
            img_urls.append(os.path.join(img_save_path,img_url))
            with open(img_urls[i],'wb') as file:
                file.write(imgs[i])
        data['success']=ac.check_in(img_urls)
        if os.path.exists(img_save_path):
            shutil.rmtree(img_save_path)
    return HttpResponse(json.dumps(data), content_type="application/json")




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
        if userID.strip()=="":
            return HttpResponse(json.dumps(data), content_type="application/json")
        save_path = os.path.join(temp_save_path, userID)
        if not os.path.exists(save_path):
            return HttpResponse(json.dumps(data), content_type="application/json")
        success=face_model.face_enter_url(userID,save_path)
        data['success']=success
        if os.path.exists(save_path):
            shutil.rmtree(save_path)
        if os.path.exists(save_path+"_temp"):
            shutil.rmtree(save_path+"_temp")

    if request.method=="POST":

        if not 'user_id' in request.POST or not 'image1' in request.POST or not 'image2' in request.POST \
                or not 'image3' in request.POST or not 'image4' in request.POST or not 'image5' in request.POST:
            return HttpResponse(json.dumps(data), content_type="application/json")
        userID=request.POST['user_id']
        if userID.strip()=="":
            return HttpResponse(json.dumps(data), content_type="application/json")
        imgs=[]
        imgs.append(base64.b64decode(request.POST['image1'].split(',')[1]))
        imgs.append(base64.b64decode(request.POST['image2'].split(',')[1]))
        imgs.append(base64.b64decode(request.POST['image3'].split(',')[1]))
        imgs.append(base64.b64decode(request.POST['image4'].split(',')[1]))
        imgs.append(base64.b64decode(request.POST['image5'].split(',')[1]))

        img_urls=[]

        save_path = os.path.join(temp_save_path, userID+"_temp")
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        usefulimg_save_path = os.path.join(temp_save_path, userID)
        if not os.path.exists(usefulimg_save_path):
            os.makedirs(usefulimg_save_path)

        img_num=len(os.listdir(save_path))
        for i in range(5):
            img_save_path=os.path.join(save_path,"{}.jpg".format(img_num+i))
            with open(img_save_path,'wb') as file:
                file.write(imgs[i])
            img_urls.append(img_save_path)
        print("img_urls:",len(img_urls))
        print(usefulimg_save_path)
        useful_count=face_model.useful_imgs(img_urls,usefulimg_save_path)
        print("useful image:",useful_count)

        data['success']=useful_count
    return HttpResponse(json.dumps(data), content_type="application/json")


def search_company(request):
    cominfo_dict = {
        'success':0,
        'companyID': '',
        'taxNumber': '',
        'bossID': '',
        'adminID': '',
        'departNames': '',
        'name': ''
    }
    # result = mm.request_join(receiver=request.POST.get('company_id'), sender=request.POST.get('user_id'), content='')
    result =cm.get_cominfo_by_id(companyID=request.POST.get('company_id'))
    if not result is None:
        cominfo_dict=result
        cominfo_dict['success']=1
    print("cominfo_dict",cominfo_dict)
    return HttpResponse(json.dumps(cominfo_dict), content_type="application/json")

def confirm_join(request):
    print("confirm join")
    data={'success':0}
    user_id = request.POST.get('user_id')
    company_id = request.POST.get('company_id')
    result = mm.request_join(receiver=company_id,sender=user_id,content='')
    print("result:",result)
    if result:
        data['success']=1
    print("data:",data)
    return HttpResponse(json.dumps(data),content_type="application/json")

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
    print(user_id)
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
    return render_to_response('camera.html')


def face_identify(request):
    data = {'success': 0}
    temp_identify_path="bigRiver/static/temp/identify"
    if not os.path.exists(temp_identify_path):
        os.makedirs(temp_identify_path)
    temp_file_num=len(os.listdir(temp_identify_path))
    img_save_path=os.path.join(temp_identify_path,"temp_{}".format(temp_file_num))
    if not os.path.exists(img_save_path):
        os.makedirs(img_save_path)
    imgs=[]
    img_urls=[]
    if request.method=="POST":
        if  not 'image1' in request.POST and not 'image2' in request.POST and not 'image3' in request.POST:
            return HttpResponse(json.dumps(data), content_type="application/json")
        imgs.append(base64.b64decode(request.POST['image1'].split(',')[1]))
        imgs.append( base64.b64decode(request.POST['image2'].split(',')[1]))
        imgs.append( base64.b64decode(request.POST['image3'].split(',')[1]))
        for i in range(3):
            img_url="{}.jpg".format(i)
            img_urls.append(os.path.join(img_save_path,img_url))
            with open(img_urls[i],'wb') as file:
                file.write(imgs[i])
        data['success']=ac.check_in(img_urls)
        shutil.rmtree(img_save_path)
    return HttpResponse(json.dumps(data), content_type="application/json")





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
<<<<<<< HEAD

def face_identify(request):
    return render_to_response("camera-identify.html")

def face_identify_login(request):
    return render_to_response("camera-identify-login.html")

def face_login(request):
    result_dict = {
        'status': False,
        'userID': 0,
        'title': 0,
    }
    temp_identify_path = "bigRiver/static/temp/identify"
    if not os.path.exists(temp_identify_path):
        os.makedirs(temp_identify_path)
    temp_file_num = len(os.listdir(temp_identify_path))
    img_save_path = os.path.join(temp_identify_path, "temp_{}".format(temp_file_num))
    if not os.path.exists(img_save_path):
        os.makedirs(img_save_path)
    imgs = []
    img_urls = []
    if request.method == "POST":
        if not 'image1' in request.POST and not 'image2' in request.POST and not 'image3' in request.POST:
            return HttpResponse(json.dumps(result_dict), content_type="application/json")
        imgs.append(base64.b64decode(request.POST['image1'].split(',')[1]))
        imgs.append(base64.b64decode(request.POST['image2'].split(',')[1]))
        imgs.append(base64.b64decode(request.POST['image3'].split(',')[1]))
        for i in range(3):
            img_url = "{}.jpg".format(i)
            img_urls.append(os.path.join(img_save_path, img_url))
            with open(img_urls[i], 'wb') as file:
                file.write(imgs[i])
        result_dict['userID'] = face_model.face_identify_urls(img_urls)
        print(result_dict['userID'])
        if result_dict['userID'] != 0:
            result_dict['status']=True
            result_dict['title']=pim.get_info_by_id(userID=result_dict['userID'])['title']
            ac.daka(result_dict['userID'])
        if os.path.exists(img_save_path):
            shutil.rmtree(img_save_path)
    return HttpResponse(json.dumps(result_dict), content_type="application/json")

def admin(request):
    return render_to_response('admin.html')
=======

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
>>>>>>> 4a88147cb3c03e3b7071daf9c918cc8104489fb8

def admin_employees(request):
    if request.method=="GET":
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
        if request.GET.get('content') == None:
            return render(request, 'admin_requests.html')
    if request.method=='POST':
        if request.POST.get('content') == 'show requests':
            print(request.POST.get('user_id'))
            user_table=mm.get_request(request.POST.get('user_id'))
            return HttpResponse(json.dumps(user_table), content_type="application/json")

def boss(request):
    return render_to_response('boss.html')

def boss_admins(request):
    if request.method=="GET":
        print("GET ", request.GET.get('content'))
        if request.GET.get('content') == None:
            return render(request, 'boss_admins.html')
        elif request.GET.get('content')=='not_boss':
            response = HttpResponseRedirect('../admin/')
            return response
    if request.method=='POST':
        if request.POST.get('content') == 'show admins':
            user_table=ac.view_all_calendar(time.strftime('%m'),time.strftime('%d'),request.POST.get('user_id'))
            return HttpResponse(json.dumps(user_table), content_type="application/json")
        elif request.POST.get('content') == 'delete admin':
            result=cm.delete_admin(pim.get_company_ID(request.POST.get('enforcer')), request.POST.get('employee'))
        elif request.POST.get('content') == 'add admin':
            result=cm.set_admin(pim.get_company_ID(request.POST.get('enforcer')), request.POST.get('employee'))
        if result:
            data='succeed'
        else:
            data='fail'
        return HttpResponse(json.dumps(data), content_type="application/json")


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
        if type=='请假':
            confirm_code=mm.send_request(sender_id,month,date,3,content)
        else:
            confirm_code = mm.send_request(sender_id, month, date, 4, content)
        if confirm_code:
            confirm_data='申请成功'
        else:
            confirm_data = '申请失败，请稍后重试'
        return HttpResponse(json.dumps(confirm_data), content_type="application/json")

def check_employee(request):
    if request.method =='GET':
        response = render_to_response('check_employee.html')
        response.set_cookie('employee_id', request.GET.get('employee_id'))
        return response

def calendar_employee(request):
    if request.method == "GET":
        return render_to_response('calendar_employee.html')
