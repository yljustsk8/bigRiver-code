import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bigRiver.settings")
django.setup()

from attendance_data.models import *
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

#对字符串进行处理
def get_new_result(old_str):
    _, _, hms, h = get_current_time()
    new_str = ''

    if(int(h)>8 and int(h)<17):
        #未在规定时间打卡
        hms += "&0"
    else:
        #在规定时间打卡
        hms += "&1"

    list = old_str.split('@')
    if (len(list) == 1):
        # 无内容或只有上班打卡
        list.insert(len(list), hms)
    elif (len(list) == 2):
        list[1] = hms
        
    for s in list:
        if (new_str):
            # 不为空
            new_str += ('@' + s)
        else:
            new_str += s
    return new_str

#获取当前时间
def get_current_time():
    nowtime = datetime.datetime.now()
    month = int(nowtime.strftime('%m'))
    date = int(nowtime.strftime('%d'))
    hms = nowtime.strftime('%H:%M:%S')
    hour = nowtime.strftime('%H')
    return month, date, hms, hour

class data(object):
    #初始化函数
    def __init__(self, userID, month='', date=''):
        self.userID = userID
        self.month, self.date, _, _ = get_current_time()
        #可能是一个debug点
        if(date != ''):
            self.date = int(date)
        if(month != ''):
            self.month = int(month)
        # 该用户本月未录入，插入新的模型
        if (len(model_list[self.month-1].objects.filter(userID=self.userID)) == 0):
            new_model = model_list[self.month-1](userID=self.userID)
            new_model.save()
        # 插入数据
        self.model = model_list[self.month-1].objects.filter(userID=self.userID)[0]
    #正常打卡
    def check(self):
        if(self.date == 1):
            self.model.day1 = get_new_result(self.model.day1)
        elif(self.date==2):
            self.model.day2 = get_new_result(self.model.day2)
        elif(self.date==3):
            self.model.day3 = get_new_result(self.model.day3)
        elif(self.date==4):
            self.model.day4 = get_new_result(self.model.day4)
        elif(self.date==5):
            self.model.day5 = get_new_result(self.model.day5)
        elif(self.date==6):
            self.model.day6 = get_new_result(self.model.day6)
        elif(self.date==7):
            self.model.day7 = get_new_result(self.model.day7)
        elif(self.date==8):
            self.model.day8 = get_new_result(self.model.day8)
        elif(self.date==9):
            self.model.day9 = get_new_result(self.model.day9)
        elif(self.date==10):
            self.model.day10 = get_new_result(self.model.day10)
        elif(self.date==11):
            self.model.day11 = get_new_result(self.model.day11)
        elif(self.date==12):
            self.model.day12 = get_new_result(self.model.day12)
        elif(self.date==13):
            self.model.day13 = get_new_result(self.model.day13)
        elif(self.date==14):
            self.model.day14 = get_new_result(self.model.day14)
        elif(self.date==15):
            self.model.day15 = get_new_result(self.model.day15)
        elif(self.date==16):
            self.model.day16 = get_new_result(self.model.day16)
        elif(self.date==17):
            self.model.day17 = get_new_result(self.model.day17)
        elif(self.date==18):
            self.model.day18 = get_new_result(self.model.day18)
        elif(self.date==19):
            self.model.day19 = get_new_result(self.model.day19)
        elif(self.date==20):
            self.model.day20 = get_new_result(self.model.day20)
        elif(self.date==21):
            self.model.day21 = get_new_result(self.model.day21)
        elif(self.date==22):
            self.model.day22 = get_new_result(self.model.day22)
        elif(self.date==23):
            self.model.day23 = get_new_result(self.model.day23)
        elif(self.date==24):
            self.model.day24 = get_new_result(self.model.day24)
        elif(self.date==25):
            self.model.day25 = get_new_result(self.model.day25)
        elif(self.date==26):
            self.model.day26 = get_new_result(self.model.day26)
        elif(self.date==27):
            self.model.day27 = get_new_result(self.model.day27)
        elif(self.date==28):
            self.model.day28 = get_new_result(self.model.day28)
        elif(self.date==29):
            self.model.day29 = get_new_result(self.model.day29)
        elif(self.date==30):
            self.model.day30 = get_new_result(self.model.day30)
        elif(self.date==31):
            self.model.day31 = get_new_result(self.model.day31)
        self.model.save()
    #补卡
    def makeup(self):
        if (self.date == 1):
            self.model.day1 = "08:00:00&1@17:00:00&1"
        elif (self.date == 2):
            self.model.day2 = "08:00:00&1@17:00:00&1"
        elif (self.date == 3):
            self.model.day3 = "08:00:00&1@17:00:00&1"
        elif (self.date == 4):
            self.model.day4 = "08:00:00&1@17:00:00&1"
        elif (self.date == 5):
            self.model.day5 = "08:00:00&1@17:00:00&1"
        elif (self.date == 6):
            self.model.day6 = "08:00:00&1@17:00:00&1"
        elif (self.date == 7):
            self.model.day7 = "08:00:00&1@17:00:00&1"
        elif (self.date == 8):
            self.model.day8 = "08:00:00&1@17:00:00&1"
        elif (self.date == 9):
            self.model.day9 = "08:00:00&1@17:00:00&1"
        elif (self.date == 10):
            self.model.day10 = "08:00:00&1@17:00:00&1"
        elif (self.date == 11):
            self.model.day11 = "08:00:00&1@17:00:00&1"
        elif (self.date == 12):
            self.model.day12 = "08:00:00&1@17:00:00&1"
        elif (self.date == 13):
            self.model.day13 = "08:00:00&1@17:00:00&1"
        elif (self.date == 14):
            self.model.day14 = "08:00:00&1@17:00:00&1"
        elif (self.date == 15):
            self.model.day15 = "08:00:00&1@17:00:00&1"
        elif (self.date == 16):
            self.model.day16 = "08:00:00&1@17:00:00&1"
        elif (self.date == 17):
            self.model.day17 = "08:00:00&1@17:00:00&1"
        elif (self.date == 18):
            self.model.day18 = "08:00:00&1@17:00:00&1"
        elif (self.date == 19):
            self.model.day19 = "08:00:00&1@17:00:00&1"
        elif (self.date == 20):
            self.model.day20 = "08:00:00&1@17:00:00&1"
        elif (self.date == 21):
            self.model.day21 = "08:00:00&1@17:00:00&1"
        elif (self.date == 22):
            self.model.day22 = "08:00:00&1@17:00:00&1"
        elif (self.date == 23):
            self.model.day23 = "08:00:00&1@17:00:00&1"
        elif (self.date == 24):
            self.model.day24 = "08:00:00&1@17:00:00&1"
        elif (self.date == 25):
            self.model.day25 = "08:00:00&1@17:00:00&1"
        elif (self.date == 26):
            self.model.day26 = "08:00:00&1@17:00:00&1"
        elif (self.date == 27):
            self.model.day27 = "08:00:00&1@17:00:00&1"
        elif (self.date == 28):
            self.model.day28 = "08:00:00&1@17:00:00&1"
        elif (self.date == 29):
            self.model.day29 = "08:00:00&1@17:00:00&1"
        elif (self.date == 30):
            self.model.day30 = "08:00:00&1@17:00:00&1"
        elif (self.date == 31):
            self.model.day31 = "08:00:00&1@17:00:00&1"
        self.model.save()
        return True
    #请假
    def leave(self):
        if (self.date == 1):
            self.model.day1 = "00:00:00&2@00:00:00&2"
        elif (self.date == 2):
            self.model.day2 = "00:00:00&2@00:00:00&2"
        elif (self.date == 3):
            self.model.day3 = "00:00:00&2@00:00:00&2"
        elif (self.date == 4):
            self.model.day4 = "00:00:00&2@00:00:00&2"
        elif (self.date == 5):
            self.model.day5 = "00:00:00&2@00:00:00&2"
        elif (self.date == 6):
            self.model.day6 = "00:00:00&2@00:00:00&2"
        elif (self.date == 7):
            self.model.day7 = "00:00:00&2@00:00:00&2"
        elif (self.date == 8):
            self.model.day8 = "00:00:00&2@00:00:00&2"
        elif (self.date == 9):
            self.model.day9 = "00:00:00&2@00:00:00&2"
        elif (self.date == 10):
            self.model.day10 = "00:00:00&2@00:00:00&2"
        elif (self.date == 11):
            self.model.day11 = "00:00:00&2@00:00:00&2"
        elif (self.date == 12):
            self.model.day12 = "00:00:00&2@00:00:00&2"
        elif (self.date == 13):
            self.model.day13 = "00:00:00&2@00:00:00&2"
        elif (self.date == 14):
            self.model.day14 = "00:00:00&2@00:00:00&2"
        elif (self.date == 15):
            self.model.day15 = "00:00:00&2@00:00:00&2"
        elif (self.date == 16):
            self.model.day16 = "00:00:00&2@00:00:00&2"
        elif (self.date == 17):
            self.model.day17 = "00:00:00&2@00:00:00&2"
        elif (self.date == 18):
            self.model.day18 = "00:00:00&2@00:00:00&2"
        elif (self.date == 19):
            self.model.day19 = "00:00:00&2@00:00:00&2"
        elif (self.date == 20):
            self.model.day20 = "00:00:00&2@00:00:00&2"
        elif (self.date == 21):
            self.model.day21 = "00:00:00&2@00:00:00&2"
        elif (self.date == 22):
            self.model.day22 = "00:00:00&2@00:00:00&2"
        elif (self.date == 23):
            self.model.day23 = "00:00:00&2@00:00:00&2"
        elif (self.date == 24):
            self.model.day24 = "00:00:00&2@00:00:00&2"
        elif (self.date == 25):
            self.model.day25 = "00:00:00&2@00:00:00&2"
        elif (self.date == 26):
            self.model.day26 = "00:00:00&2@00:00:00&2"
        elif (self.date == 27):
            self.model.day27 = "00:00:00&2@00:00:00&2"
        elif (self.date == 28):
            self.model.day28 = "00:00:00&2@00:00:00&2"
        elif (self.date == 29):
            self.model.day29 = "00:00:00&2@00:00:00&2"
        elif (self.date == 30):
            self.model.day30 = "00:00:00&2@00:00:00&2"
        elif (self.date == 31):
            self.model.day31 = "00:00:00&2@00:00:00&2"
        self.model.save()
        return True
