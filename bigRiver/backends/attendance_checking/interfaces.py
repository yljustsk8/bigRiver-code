import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bigRiver.settings")
django.setup()

from backends.attendance_checking import insert, get_calendar
from attendance_data.models import *
from backends.ai.interfaces import *
from backends.personal_info_management import interfaces as pim
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
    result = get_calendar.get_month_calendar(month, userID, query_title='3')
    return result

#查看单个员工单年日历
def view_single_year_calendar(userID):
    result_dict = {}
    for month in range(12):
        result_dict[month+1] = view_single_calendar(month+1, uid=userID)
    for month in range(12):
        for date in range(31):
            if(result_dict[month+1][date+1]==''):
                result_dict[month + 1][date + 1] = '00:00&3@00:00&3'
            result_dict[month+1][date+1] = str(month+1).rjust(2, '0')+str(date+1).rjust(2, '0')+'@'+result_dict[month+1][date+1]
        # result += view_single_calendar(month+1, uid=userID)
    return result_dict

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
def view_all_calendar(m, d, uid):
    month = int(m)
    date = int(d)
    userID = uid
    info_dict = pim.get_info_by_id(userID=userID)
    company = info_dict['company']
    title = info_dict['title']
    result_dict = get_calendar.get_daily_calendar(month=month, date=date, company=company, query_title=title)
    # print(result_dict)
    result = {
        'count': 10,
        'info': []
    }

    i = 1
    for key, value in result_dict.items():
        info_dict_tmp = pim.get_info_by_id(userID=key)
        t = info_dict_tmp['title']
        # value的值模板：07:40&1@17:02&1
        # print(key + ': ' + str(t))
        # 决定title_rt的值
        if(str(t)=='1'):
            title_rt = '普通员工'
        elif(str(t)=='2'):
            title_rt = '管理员'
        elif(str(t)=='3'):
            title_rt = '老板'
        else:
            title_rt = '异常值'
        # 决定status的值
        status = ''
        if(value):
            # 读取时间和状态
            l = value.split('@')
            t1 = l[0].split('&')[0]
            status1 = int(l[0].split('&')[1])
            t2 = l[1].split('&')[0]
            status2 = int(l[1].split('&')[1])
            if(status1==1 and status2==1):
                status = '正常出席'
            elif(status1==0 and status2==1):
                status = '迟到'
            elif(status1==1 and status2==0):
                status = '早退'
            elif(status1==0 and status2==0):
                status = '迟到早退'
            elif(status1==2 and status2==2):
                status = '请假'
        else:
            t1 = ''
            t2 = ''
            status = '未打卡'
        #构造result字典
        attendance_dict = {
            'user_id': key,
            'name': info_dict_tmp['name'],
            'dpmt': info_dict_tmp['department'],
            'time_in': t1,
            'time_out': t2,
            'status': status,
            'title': title_rt
        }
        #插入
        result['info'].insert(len(result['info']), attendance_dict)

    # print(result)
    return result

if(__name__=='__main__'):
    # view_all_calendar(8, 31, '10001')
    print(view_single_year_calendar('1000010'))
