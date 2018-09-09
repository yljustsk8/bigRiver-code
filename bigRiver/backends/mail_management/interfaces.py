from request_data.models import requests
from backends.personal_info_management import interfaces as pim
from backends.attendance_checking import interfaces as ac
from backends.mail_management import inside_func as inf
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

msg_type = ['申请加入', '邀请加入', '申请请假', '申请补卡']


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

# 接口1：发出"加入公司"申请 输入：发送者ID，接收公司ID，内容
def request_join(receiver, sender, content):
    # 构建模型，将请求插入数据库
    the_model = requests(requestID=inf.get_requestID(),
                         receiverID=receiver,
                         senderID=sender,
                         date=inf.get_date(),
                         type=1,
                         content=content,
                         dealed=False,
                         result=-1)
    the_model.save()
    return True

# 接口2：发出"邀请加入公司"申请 输入：发送者公司ID，接收者ID，内容
def send_invitation(receiver, sender, content):
    # 构建模型，将请求插入数据库
    the_model = requests(requestID=inf.get_requestID(),
                         receiverID=receiver,
                         senderID=sender,
                         date=inf.get_date(),
                         type=2,
                         content=content,
                         dealed=False,
                         result=-1)
    the_model.save()
    return True

# 接口3：发出"请假/补卡"申请 输入：申请者ID，申请请假/补卡的月/日，申请类型（3：请假，4：补卡），内容
def send_request(sender, month, date, type, content):
    #t=3 请假申请，t=4 补卡申请
    the_date = str(month) + '@' + str(date)
    receiver = pim.get_company_ID(userID=sender)
    the_model = requests(requestID=inf.get_requestID(),
                         receiverID=receiver,
                         senderID=sender,
                         date=inf.get_date(),
                         type=type,
                         content=content,
                         dealed=False,
                         result=-1,
                         requestdate=the_date)
    the_model.save()
    return True

# 接口4：处理"申请加入"
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
    requestID = rID
    result = r
    if(handle_request(requestID, result)):
        #更改消息条目本身
        the_model = requests.objects.get(requestID=requestID)
        stuff_id = the_model.senderID
        company_id = the_model.receiverID
        month = the_model.requestdate.split('@')[0]
        date = the_model.requestdate.split('@')[1]
        if(result):
            #执行操作
            if(the_model.type == 3):
                #请假
                ac.do_leave(uid=stuff_id, m=month, d=date)
            elif(the_model.type == 4):
                #补卡
                ac.do_makeup(uid=stuff_id, m=month, d=date)
    return True

def get_request(uID):
    _,_,_,title,_ = pim.get_info_by_id(uID)
    if(title == 0 or title == 1):
        #普通用户
        receive_list = requests.objects.filter(receiverID=uID)
        send_list = requests.objects.filter(senderID=uID)
        the_list = receive_list + send_list
    elif(title == 2 or title == 3):
        # 管理员/boss
        company_id = pim.get_company_ID(uID)
        receive_list = requests.objects.filter(receiverID=company_id)
        send_list = requests.objects.filter(senderID=uID)
        # the_list = receive_list + send_list
    result = {'count':len(receive_list) + len(send_list),
              'info':[]}
    # 收到的
    for msg in receive_list:
        name,_,department,_,_ = pim.get_info_by_id(msg.senderID)
        msg_dict = {
                        'request_id': msg.requestID,
                        'user_id': msg.senderID,
                        'name': name,
                        'dpmt': department,
                        'type': msg_type[msg.type-1]
                    }
        result['info'].insert(len(result['info']), msg_dict)
    # 发出的
    for msg in send_list:
        name, _, department, _, _ = pim.get_info_by_id(msg.receiverID)
        msg_dict = {
            'request_id': msg.requestID,
            'user_id': msg.receiverID,
            'name': name,
            'dpmt': department,
            'type': msg_type[msg.type - 1]
        }
        result['info'].insert(len(result['info']), msg_dict)
    print(result)
    return result
