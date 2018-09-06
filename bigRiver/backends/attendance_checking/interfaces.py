import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bigRiver.settings")
django.setup()

from backends.attendance_checking import insert, get_calendar
from attendance_data.models import *
from backends.ai.interfaces import *
import cv2
import datetime


# 考勤打卡模块:
# 1.	userID check_in（图片）调用 人脸识别模块函数 face_identify，调用
# 假设 check_in_info { info[][2]  第一列是userID，第二列是时间 格式为yy/mm/dd-hh:mm:ss@yy/mm/dd-hh:mm:ss,分别为上班打卡和下班打卡}
# 2.	所有员工打卡信息 view_all_calendar（date）
# 3.	单个员工打卡信息 view_single_calendar（userID,month）
# 4.	bool ask_for_makeup(userID,date)
# 5.	bool ask_for_leave(userID,date)
#

#正常打卡
def check_in(img_url):
    img = cv2.imread(img_url)
    userID = face_identify(img)
    print(userID)
    if(userID):
        #识别成功
        the_data = insert.data(userID=userID)
        the_data.check()
    else:
        return False

#查看单个员工单月日历
def view_single_calendar(m, uid):
    month = m
    userID = uid
    result = get_calendar.get_month_calendar(month, userID)
    return result

#补卡
def do_makeup(uid, m, d):
    #执行补卡操作
    userID = uid
    month = m
    date = d
    the_data = insert.data(userID=userID, month=month, date=date)
    return the_data.makeup()

#请假
def do_leave(uid, m, d):
    #执行请假操作
    userID = uid
    month = m
    date = d
    the_data = insert.data(userID=userID, month=month, date=date)
    return the_data.leave()

#查看公司员工单日日历
def view_all_calendar(m, d, c):
    month = m
    date = d
    company = c
    result = get_calendar.get_daily_calendar(month=month, date=date, company=company)
    return result


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

