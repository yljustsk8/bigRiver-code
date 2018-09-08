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
