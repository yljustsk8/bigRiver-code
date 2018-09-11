import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bigRiver.settings")
django.setup()

from attendance_data.models import *
from basic_info.models import *
from backends.personal_info_management import interfaces as pim
import datetime

model_list = [attendance_data_jan,
              attendance_data_feb,
              attendance_data_mar,
              attendance_data_apr,
              attendance_data_may,
              attendance_data_jun,
              attendance_data_july,
              attendance_data_aug,
              attendance_data_sep,
              attendance_data_oct,
              attendance_data_nov,
              attendance_data_dec]

def get_month_calendar(month, userID, query_title):
    model = model_list[month-1]
    #判断其是否为普通员工，若是，则查看其数据。
    title = pim.get_info_by_id(userID=userID)['title']
    if(int(query_title)<=int(title)):
        #不为普通员工
        result_list = []
        return result_list
    # 为普通员工
    if not (model.objects.filter(userID=userID)):
        new_model = model(userID=userID)
        new_model.save()
    user_model = model.objects.filter(userID=userID)[0]
    result_list = [userID]
    result_list.append(user_model.day1)
    result_list.append(user_model.day2)
    result_list.append(user_model.day3)
    result_list.append(user_model.day4)
    result_list.append(user_model.day5)
    result_list.append(user_model.day6)
    result_list.append(user_model.day7)
    result_list.append(user_model.day8)
    result_list.append(user_model.day9)
    result_list.append(user_model.day10)
    result_list.append(user_model.day11)
    result_list.append(user_model.day12)
    result_list.append(user_model.day13)
    result_list.append(user_model.day14)
    result_list.append(user_model.day15)
    result_list.append(user_model.day16)
    result_list.append(user_model.day17)
    result_list.append(user_model.day18)
    result_list.append(user_model.day19)
    result_list.append(user_model.day20)
    result_list.append(user_model.day21)
    result_list.append(user_model.day22)
    result_list.append(user_model.day23)
    result_list.append(user_model.day24)
    result_list.append(user_model.day25)
    result_list.append(user_model.day26)
    result_list.append(user_model.day27)
    result_list.append(user_model.day28)
    result_list.append(user_model.day29)
    result_list.append(user_model.day30)
    result_list.append(user_model.day31)
    return result_list

def get_daily_calendar(month, date, company, query_title):
    stuff_list = personal_info.objects.filter(company=company)
    stuff_id_list = []
    result_dict = dict()
    for s in stuff_list:
        #填充员工列表
        # print(s.userID)
        stuff_id_list.append(s.userID)
    # print(stuff_list)
    for sid in stuff_id_list:
        # print(sid)
        result_list = get_month_calendar(month, sid, query_title)
        # print(result_list)
        if(len(result_list)):
            # print("in len ")
            result_dict[sid] = result_list[date]
    return result_dict
