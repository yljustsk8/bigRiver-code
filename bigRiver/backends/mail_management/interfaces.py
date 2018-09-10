from request_data.models import requests
from backends.personal_info_management import interfaces as pim
from backends.attendance_checking import interfaces as ac
from backends.mail_management import inside_func as inf
from backends.company_management import interfaces as cm
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

# 接口4：处理"申请加入" 输入：响应请求的ID，响应的结果：若同意则为1，反之为0
# 返回布尔值
def answer_join(requestID, result):
    if(inf.handle_request(requestID, result)):
        #更改消息条目
        the_model = requests.objects.get(requestID=requestID)
        stuff_id = the_model.senderID
        company_id = the_model.receiverID
        if(result):
            #更新员工所在公司
            if(pim.join_company(stuffID=stuff_id, companyID=company_id)):
                return True
            else:
                return False
        else:
            #不进行变更，仅处理消息
            return True
    else:
        return False

# 接口5：处理"邀请加入" 输入：响应请求的ID，响应的结果：若同意则为1，反之为0
# 返回布尔值
def answer_invitation(requestID, result):
    if(inf.handle_request(requestID, result)):
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

# 接口6：处理"请假、补卡" 输入：
def answer_other_req(rID, r):
    requestID = rID
    result = r
    if(inf.handle_request(requestID, result)):
        #更改消息条目本身
        the_model = requests.objects.get(requestID=requestID)
        stuff_id = the_model.senderID
        company_id = the_model.receiverID
        month = the_model.requestdate.split('@')[0]
        date = the_model.requestdate.split('@')[1]
        print(the_model.requestdate)
        if(result):
            #执行操作
            if(the_model.type == 3):
                #请假
                ac.do_leave(uid=stuff_id, m=month, d=date)
            elif(the_model.type == 4):
                #补卡
                ac.do_makeup(uid=stuff_id, m=month, d=date)
    return True

# 接口7：输入：请求的用户ID
# 返回：该用户若为普通员工或无公司员工，则返回该员工的私人消息字典
#      该用户若为管理员或boss，则返回该公司的公共消息字典
def get_request(uID):
    title = pim.get_info_by_id(uID)['title']
    if(title == 0 or title == 1):
        #普通用户
        receive_list = requests.objects.filter(receiverID=uID)
        send_list = requests.objects.filter(senderID=uID)
        the_list = receive_list + send_list
    elif(title == 2 or title == 3):
        # 管理员/boss
        company_id = pim.get_company_ID(uID)
        receive_list = requests.objects.filter(receiverID=company_id)
        print(receive_list)
        send_list = requests.objects.filter(senderID=company_id)
        print(send_list)
        # the_list = receive_list + send_list
    result = {'count':10,
              'info':[]}
    # 收到的
    for msg in receive_list:
        if(msg.type == 2):
            name = cm.get_cominfo_by_id(msg.senderID)['name']
            department = ''
        else:
            info_dict = pim.get_info_by_id(msg.senderID)
            name = info_dict['name']
            department = info_dict['departmentName']
        msg_dict = {
                        'request_id': msg.requestID,
                        'user_id': msg.senderID,
                        'name': name,
                        'dpmt': department,
                        'type': msg_type[msg.type-1],
                        'content': msg.content
                    }
        result['info'].insert(len(result['info']), msg_dict)
    # 发出的
    for msg in send_list:
        if(msg.type == 2):
            name = cm.get_cominfo_by_id(msg.senderID)['name']
            department = ''
        else:
            info_dict = pim.get_info_by_id(msg.senderID)
            name = info_dict['name']
            department = info_dict['departmentName']
        msg_dict = {
            'request_id': msg.requestID,
            'user_id': msg.receiverID,
            'name': name,
            'dpmt': department,
            'type': msg_type[msg.type - 1],
            'content': msg.content
        }
        result['info'].insert(len(result['info']), msg_dict)
    print(result)
    return result
