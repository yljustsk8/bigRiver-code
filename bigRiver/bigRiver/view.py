from django.shortcuts import render,HttpResponse,redirect,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from backends.personal_info_management import interfaces as pim
from backends.company_management import interfaces as cm
from backends.attendance_checking import interfaces as ac
from backends.mail_management import interfaces as mm
import json
import base64
import os
import time

from backends.ai.face_model import save_face
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
    if request.method=="GET":
        return render_to_response("login.html");
    if request.method=="POST":
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        name = request.POST.get('name')
        email = request.POST.get('e-mail')
        result = pim.register(user_id, password, name, email)
        if result['status']:
            return HttpResponse(True)
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
    if request.method =='GET':
        return render_to_response("create_company.html")
    if request.method =='POST':
        user_id = request.POST.get('user_id')
        company_name = request.POST.get('company_name')
        taxNumber = request.POST.get('taxNumber')
        result = pim.create_company(user_id, company_name, taxNumber)
        if result['status']:
            return HttpResponse(True)
        else:
            return HttpResponse(result['content'])



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
    result_dict = pim.get_info_by_id(user_id)
    result = {'name': result_dict['name'],
              'email':result_dict['email'],
              'password':result_dict['password'],}
    return HttpResponse(json.dumps(result), content_type="application/json")


def about_us(request):
    return render_to_response("BOT.html")

def calendar(request):
    if request.method == "GET":
        return render_to_response('calendar.html')
    if request.method == "POST":
        user_id=request.POST.get('user_id')
        # result=ac.view_single_calendar(month, user_id)
        result={1: ['1000010', '0101@', '0102@', '0103@', '0104@', '0105@', '0106@', '0107@', '0108@', '0109@', '0110@', '0111@', '0112@', '0113@', '0114@', '0115@', '0116@', '0117@', '0118@', '0119@', '0120@', '0121@', '0122@', '0123@', '0124@', '0125@', '0126@', '0127@', '0128@', '0129@', '0130@', '0131@'],
                2: ['1000010', '0201@', '0202@', '0203@', '0204@', '0205@', '0206@', '0207@', '0208@', '0209@', '0210@', '0211@', '0212@', '0213@', '0214@', '0215@', '0216@', '0217@', '0218@', '0219@', '0220@', '0221@', '0222@', '0223@', '0224@', '0225@', '0226@', '0227@', '0228@', '0229@', '0230@', '0231@'],
                3: ['1000010', '0301@', '0302@', '0303@', '0304@', '0305@', '0306@', '0307@', '0308@', '0309@', '0310@', '0311@', '0312@', '0313@', '0314@', '0315@', '0316@', '0317@', '0318@', '0319@', '0320@', '0321@', '0322@', '0323@', '0324@', '0325@', '0326@', '0327@', '0328@', '0329@', '0330@', '0331@'],
                4: ['1000010', '0401@', '0402@', '0403@', '0404@', '0405@', '0406@', '0407@', '0408@', '0409@', '0410@', '0411@', '0412@', '0413@', '0414@', '0415@', '0416@', '0417@', '0418@', '0419@', '0420@', '0421@', '0422@', '0423@', '0424@', '0425@', '0426@', '0427@', '0428@', '0429@', '0430@', '0431@'],
                5: ['1000010', '0501@', '0502@', '0503@', '0504@', '0505@', '0506@', '0507@', '0508@', '0509@', '0510@', '0511@', '0512@', '0513@', '0514@', '0515@', '0516@', '0517@', '0518@', '0519@', '0520@', '0521@', '0522@', '0523@', '0524@', '0525@', '0526@', '0527@', '0528@', '0529@', '0530@', '0531@'],
                6: ['1000010', '0601@', '0602@', '0603@', '0604@', '0605@', '0606@', '0607@', '0608@', '0609@', '0610@', '0611@', '0612@', '0613@', '0614@', '0615@', '0616@', '0617@', '0618@', '0619@', '0620@', '0621@', '0622@', '0623@', '0624@', '0625@', '0626@', '0627@', '0628@', '0629@', '0630@', '0631@'],
                7: ['1000010', '0701@', '0702@', '0703@', '0704@', '0705@', '0706@', '0707@', '0708@', '0709@', '0710@', '0711@', '0712@', '0713@', '0714@', '0715@', '0716@', '0717@', '0718@', '0719@', '0720@', '0721@', '0722@', '0723@', '0724@', '0725@', '0726@', '0727@', '0728@', '0729@', '0730@', '0731@'],
                8: ['1000010', '0801@07:40&1@17:02&1', '0802@08:40&1@17:02&1', '0803@07:45&1@18:02&1', '0804@07:45&1@17:02&1', '0805@00:00&1@17:02&1', '0806@07:45&1@17:02&1', '0807@07:450&1@17:02&1', '0808@07:40&1@17:02&1', '0809@07:40&1@17:02&1', '0810@00:00&2@00:00&2', '0811@08:10&0@17:05&1', '0812@07:42&1@16:30&0', '0813@08:25&0@16:40&0', '0814@07:52&1@17:02&1', '0815@07:52&1@17:02&1', '0816@07:52&1@17:02&1', '0817@07:52&1@17:02&1', '0818@07:52&1@17:13&1', '0819@07:40&1@17:13&1', '0820@07:40&1@17:13&1', '0821@07:40&1@17:13&1', '0822@07:40&1@17:13&1', '0823@07:40&1@17:13&1', '0824@07:40&1@17:13&1', '0825@07:40&1@17:02&1', '0826@07:40&1@17:02&1', '0827@07:40&1@17:02&1', '0828@07:40&1@17:02&1', '0829@07:40&1@17:02&1', '0830@07:40&1@17:02&1', '0831@07:40&1@17:02&1'],
                9: ['1000010', '0901@', '0902@', '0903@', '0904@', '0905@', '0906@', '0907@', '0908@', '0909@', '0910@', '0911@', '0912@', '0913@', '0914@', '0915@', '0916@', '0917@', '0918@', '0919@', '0920@', '0921@', '0922@', '0923@', '0924@', '0925@', '0926@', '0927@', '0928@', '0929@', '0930@', '0931@'],
                10: ['1000010', '1001@', '1002@', '1003@', '1004@', '1005@', '1006@', '1007@', '1008@', '1009@', '1010@', '1011@', '1012@', '1013@', '1014@', '1015@', '1016@', '1017@', '1018@', '1019@', '1020@', '1021@', '1022@', '1023@', '1024@', '1025@', '1026@', '1027@', '1028@', '1029@', '1030@', '1031@'],
                11: ['1000010', '1101@', '1102@', '1103@', '1104@', '1105@', '1106@', '1107@', '1108@', '1109@', '1110@', '1111@', '1112@', '1113@', '1114@', '1115@', '1116@', '1117@', '1118@', '1119@', '1120@', '1121@', '1122@', '1123@', '1124@', '1125@', '1126@', '1127@', '1128@', '1129@', '1130@', '1131@'],
                12: ['1000010', '1201@', '1202@', '1203@', '1204@', '1205@', '1206@', '1207@', '1208@', '1209@', '1210@', '1211@', '1212@', '1213@', '1214@', '1215@', '1216@', '1217@', '1218@', '1219@', '1220@', '1221@', '1222@', '1223@', '1224@', '1225@', '1226@', '1227@', '1228@', '1229@', '1230@', '1231@']}
        return HttpResponse(json.dumps(result), content_type="application/json")


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
            print("here")
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
