from request_data.models import requests
from backends.personal_info_management import interfaces as pim
from backends.attendance_checking import interfaces as ac
import datetime

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
def handle_request(requestID, result):
    #作为request的单元处理
    select_result = requests.objects.filter(requestID=requestID)
    if not select_result:
        print("request doesn't exist!")
        return False
    else:
        the_model = select_result[0]
    print('in handle_request:'+the_model.requestID)
    the_model.dealed = True
    if(result):
        the_model.result=1
    else:
        the_model.result=0
    the_model.save()
    return True
