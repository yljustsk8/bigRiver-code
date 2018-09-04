from request_data.models import requests
from backends.personal_info_management import interfaces as pim
import datetime
# 1.	bool send_invitation(userID,companyID)
# 2.	bool answer_invitation(requestID, bool)
# 3.	bool send_request(userID,date,type)
# 4.	List<requestID> show_requests()
# 5.	bool handle_request(requestID, bool)
# 6.	< userID,companyID ,bool > fetch_request(requestID)
# 7.    bool delete_msg
#申请加入   type=1  senderID = userID  receiverID = companyID
#邀请加入   type=2  senderID = companyID  receiverID = userID
#申请请假   type=3  senderID = userID  receiverID = companyID
#申请补卡   type=4  senderID = userID  receiverID = companyID

#获取当前日期
def get_date():
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    return date

#获取当前requestID
def get_requestID():
    entire_model = requests.objects.all()
    l = len(entire_model)
    new_request_id = int(entire_model[l - 1].requestID) + 1
    return new_request_id

#处理所有请求的接口
def handle_request(rID, r):
    #作为request的单元处理
    requestID = rID
    result = r
    select_result = requests.objects.filter(requestID=requestID)
    if not select_result:
        print("request doesn't exist!")
        return False
    else:
        the_model = select_result[0]

    the_model.dealed = True
    if(result):
        the_model.result=1
    else:
        the_model.result=0
    return True

#申请加入公司
def request_join(rID, cID, c):
    receiver = cID
    sender = rID
    content = c
    the_model = requests(requestID=get_requestID(),
                         receiverID=receiver,
                         senderID=sender,
                         date=get_date(),
                         type=1,
                         content=content,
                         dealed=False,
                         result=-1)
    the_model.save()
    return True

#邀请加入公司
def send_invitation(u, c):
    receiver = u
    sender = c
    #存入model
    the_model = requests(requestID=get_requestID(),
                         receiverID=receiver,
                         senderID=sender,
                         date=get_date(),
                         type=2,
                         content='send_invitation',
                         dealed=False,
                         result=-1)
    the_model.save()
    return True

#申请请假、补卡
def send_request(uID, d, t, c):
    #t=3 请假申请，t=4 补卡申请
    sender = uID
    receiver = pim.get_company_ID(userID=sender)
    type = t
    content = c
    the_model = requests(requestID=get_requestID(),
                         receiverID=receiver,
                         senderID=sender,
                         date=get_date(),
                         type=type,
                         content=content,
                         dealed=False,
                         result=-1)
    the_model.save()

#处理"申请加入"
def answer_join(rID, r):
    requestID = rID
    result = r
    if(handle_request(requestID, result)):
        #更改消息条目
        the_model = requests.objects.get(requestID=requestID)
        stuff_id = the_model.senderID
        company_id = the_model.receiverID
        if(result):
            #更新公司
            if(pim.join_company(stuffID=stuff_id, companyID=company_id)):
                return True
            else:
                return False
        else:
            #不进行变更，仅处理消息
            return True
    else:
        return False

#处理"邀请加入"
def answer_invitation(rID, r):
    #用户同意
    requestID = rID
    result = r
    if(handle_request(requestID, result)):
        #更改消息条目本身
        the_model = requests.objects.get(requestID=requestID)
        stuff_id = the_model.receiverID
        company_id = the_model.senderID
        if(result):
            #更新公司
            if(pim.join_company(stuffID=stuff_id, companyID=company_id)):
                return True
            else:
                return False
        else:
            #不进行变更，仅处理消息
            return True
    else:
        #更改出现错误
        return False

#处理"请假、补卡"
def answer_other_req(rID, r):
    #打卡模块结束后编写
    return True

def get_request(uID):
    _,_,_,title,_ = pim.get_info_by_id(uID)
    if(title == 0 or title == 1):
        #普通用户
        receive_list = requests.objects.filter(receiverID=uID)
        send_list = requests.objects.filter(senderID=uID)
        the_list = receive_list + send_list
    elif(title == 2 or title == 3):
        #管理员/boss
        company_id = pim.get_company_ID(uID)
        receive_list = requests.objects.filter(receiverID=company_id)
        send_list = requests.objects.filter(senderID=uID)
        the_list = receive_list + send_list
    return the_list
