import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bigRiver.settings")
django.setup()

from attendance_data.models import *
from basic_info.models import *
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

def get_month_calendar(month, userID):
    model = model_list[month-1]
    user_model = model.objects.filter(userID=userID)[0]
    result_list = [userID]
    result_list[1] = user_model.day1
    result_list[2] = user_model.day2
    result_list[3] = user_model.day3
    result_list[4] = user_model.day4
    result_list[5] = user_model.day5
    result_list[6] = user_model.day6
    result_list[7] = user_model.day7
    result_list[8] = user_model.day8
    result_list[9] = user_model.day9
    result_list[10] = user_model.day10
    result_list[11] = user_model.day11
    result_list[12] = user_model.day12
    result_list[13] = user_model.day13
    result_list[14] = user_model.day14
    result_list[15] = user_model.day15
    result_list[16] = user_model.day16
    result_list[17] = user_model.day17
    result_list[18] = user_model.day18
    result_list[19] = user_model.day19
    result_list[20] = user_model.day20
    result_list[21] = user_model.day21
    result_list[22] = user_model.day22
    result_list[23] = user_model.day23
    result_list[24] = user_model.day24
    result_list[25] = user_model.day25
    result_list[26] = user_model.day26
    result_list[27] = user_model.day27
    result_list[28] = user_model.day28
    result_list[29] = user_model.day29
    result_list[30] = user_model.day30
    result_list[31] = user_model.day31
    return result_list

def get_daily_calendar(month, date, company):
    stuff_list = personal_info.objects.filter(company=company)
    stuff_id_list = []
    result_dict = dict()
    for s in stuff_list:
        #填充员工列表
        stuff_id_list.insert(len(stuff_id_list), s.userID)
    for sid in stuff_id_list:
        result_dict[sid] = get_month_calendar(month, sid)[date-1]
    return result_dict
